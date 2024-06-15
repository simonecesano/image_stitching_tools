import sys
import cv2
import argparse
import tempfile

parser = argparse.ArgumentParser(
                    prog='stitch_images',
                    description='Stitches images together')

parser.add_argument('image_files', nargs='+', help='files to be cropped')
parser.add_argument('-r', '--reference', help='file whose position must be defined')
parser.add_argument('-c', '--container', help='file containing the reference file')
parser.add_argument('-d', '--display', action='store_true', help='display cropped file')
parser.add_argument('-o', '--output', default="stitched.png")
parser.add_argument('-p', '--pairwise', action='store_true', help='try stitching pairwise')
parser.add_argument('-C', '--cautious', action='store_true', help='use cautious algorithm')
parser.add_argument('-v', '--verbose', action='store_true', help='print more stuff')

args = parser.parse_args()



# print(tempfile.NamedTemporaryFile(suffix=".png").name)
# exit()

stitcher = cv2.Stitcher.create(mode=1)
images = [ { "name": i, "image":  cv2.imread(i)} for i in args.image_files ]

if args.pairwise:
    import networkx as nx
    G = nx.Graph()
    for a in images:
        G.add_node(a["name"])
        for b in [ b for b in images if a["name"] != b["name"] ]:
            (status, stitched) = stitcher.stitch([ a["image"], b["image"] ])
            print(a["name"], b["name"], status == cv2.Stitcher_OK)
            if status == cv2.Stitcher_OK:
                G.add_edge(a["name"], b["name"])
    for l in list(nx.connected_components(G)):
        print(l)
        # insert groupwise stitching here
    exit()

if args.cautious:
    i = 1
    template = args.output.replace(".", "_{:02d}.")
    for a in images:
        for b in [ b for b in images if a["name"] != b["name"] ]:
            outfile = template.format(i)
            i = i + 1 
            (status, stitched) = stitcher.stitch([ i["image"] for i in images ])
            if status == cv2.Stitcher_OK:
                print("writing to " + outfile)
                cv2.imwrite(outfile, stitched)
                
    exit()
    pass


(status, stitched) = stitcher.stitch([ i["image"] for i in images ])

if status == cv2.Stitcher_OK:
    cv2.imwrite(args.output, stitched)
else:
    print("Can't stitch images, error code = %d" % status)
    sys.exit(-1)
