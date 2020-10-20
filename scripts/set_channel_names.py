import pandas
import os
import sys
import omero
from omero.gateway import BlitzGateway

host = os.environ.get('OMERO_HOST', 'localhost')
port = int(os.environ.get('OMERO_PORT', '4064'))

df = pandas.read_csv(sys.argv[1])
channel_names = {}

for index, row in df.iterrows():
    key = "{},{}".format(row["Plate"], row["Well"])
    # Ch1 (blue): Nuclei/Cytoplasm, Ch2 (green): ACTB, Ch3 (red): RAB5A
    ch1 = None
    ch2 = None
    ch3 = None
    for channel_info in row["Channels"].split(","):
        idx = channel_info.index(":") + 1
        channel_name = channel_info[idx:].strip()
        if channel_info.strip().startswith("Ch1"):
            ch1 = channel_name
        elif channel_info.strip().startswith("Ch2"):
            ch2 = channel_name
        elif channel_info.strip().startswith("Ch3"):
            ch3 = channel_name
    if not (ch1 and ch2 and ch3):
        print("Channel name missing for row {}".format(index))
    channel_names[key] = {1: ch1, 2: ch2, 3: ch3}


conn = BlitzGateway(os.environ.get('OMERO_USER', 'xxx'),
                    os.environ.get('OMERO_PASSWORD', 'xxx'),
                    host=host, port=port)
conn.connect()

screen = conn.getObject("Screen", sys.argv[2])
for pl in screen.listChildren():
    n_fields = pl.getNumberOfFields()
    for well in pl.listChildren():
        print("Processing {} - {}".format(pl.getName(), well.getWellPos()))
        for field in range(n_fields[0], n_fields[1] + 1):
             ws = well.getWellSample(field)
             key = "{},{}".format(pl.getName(), well.getWellPos())
             if ws and ws.getImage() and key in channel_names:
                img = well.getImage()
                conn.setChannelNames("Image", [img.getId()], channel_names[key],
                                     channelCount=None)

conn.close()

