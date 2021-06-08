"""
MobileNet-SSD Toolkits: merge_bn.py

@Author:    qinhongjie@imilab.com
@Data:      2021/05/25

Usage:
$ python merge_bn.py --pycaffe $HOME/desktop/caffe/python --model deploy.prototxt --weights mobilenet_ssd.caffemodel --model_out out.prototxt --weights_out out.caffemodel
"""

import argparse
import sys, os
import numpy as np

## default settings
DIR_ROOT = os.path.dirname(os.path.abspath(__file__))
DIR_PYCAFFE = os.path.join(DIR_ROOT, "../../../python")

bn_maps = {}
def find_top_after_bn(layers, name, top):
    bn_maps[name] = {} 
    for l in layers:
        if len(l.bottom) == 0:
            continue
        if l.bottom[0] == top and l.type == "BatchNorm":
            bn_maps[name]["bn"] = l.name
            top = l.top[0]
        if l.bottom[0] == top and l.type == "Scale":
            bn_maps[name]["scale"] = l.name
            top = l.top[0]
    return top


def pre_process(expected_proto, new_proto):

    from caffe.proto import caffe_pb2
    from google.protobuf import text_format

    net_specs = caffe_pb2.NetParameter()
    net_specs2 = caffe_pb2.NetParameter()
    with open(expected_proto, "r") as fp:
        text_format.Merge(str(fp.read()), net_specs)

    net_specs2.MergeFrom(net_specs)
    layers = net_specs.layer
    num_layers = len(layers)

    for i in range(num_layers - 1, -1, -1):
         del net_specs2.layer[i]

    for idx in range(num_layers):
        l = layers[idx]
        if l.type == "BatchNorm" or l.type == "Scale":
            continue
        elif l.type == "Convolution" or l.type == "Deconvolution":
            top = find_top_after_bn(layers, l.name, l.top[0])
            bn_maps[l.name]["type"] = l.type
            layer = net_specs2.layer.add()
            layer.MergeFrom(l)
            layer.top[0] = top
            layer.convolution_param.bias_term = True
        else:
            layer = net_specs2.layer.add()
            layer.MergeFrom(l)

    with open(new_proto, "w") as fp:
        fp.write("{}".format(net_specs2))


def load_weights(net, nobn):
    if sys.version_info > (3,0):
        listKeys = nobn.params.keys()
    else:
        listKeys = nobn.params.iterkeys()
    for key in listKeys:
        if type(nobn.params[key]) is caffe._caffe.BlobVec:
            conv = net.params[key]
            if key not in bn_maps or "bn" not in bn_maps[key]:
                for i, w in enumerate(conv):
                    nobn.params[key][i].data[...] = w.data
            else:
                print(key)
                bn = net.params[bn_maps[key]["bn"]]
                scale = net.params[bn_maps[key]["scale"]]
                wt = conv[0].data
                channels = 0
                if bn_maps[key]["type"] == "Convolution": 
                    channels = wt.shape[0]
                elif bn_maps[key]["type"] == "Deconvolution": 
                    channels = wt.shape[1]
                else:
                    print("error type " + bn_maps[key]["type"])
                    exit(-1)
                bias = np.zeros(channels)
                if len(conv) > 1:
                    bias = conv[1].data
                mean = bn[0].data
                var = bn[1].data
                scalef = bn[2].data

                scales = scale[0].data
                shift = scale[1].data

                if scalef != 0:
                    scalef = 1. / scalef
                mean = mean * scalef
                var = var * scalef
                rstd = 1. / np.sqrt(var + 1e-5)
                if bn_maps[key]["type"] == "Convolution": 
                    rstd1 = rstd.reshape((channels,1,1,1))
                    scales1 = scales.reshape((channels,1,1,1))
                    wt = wt * rstd1 * scales1
                else:
                    rstd1 = rstd.reshape((1, channels,1,1))
                    scales1 = scales.reshape((1, channels,1,1))
                    wt = wt * rstd1 * scales1
                bias = (bias - mean) * rstd * scales + shift
                
                nobn.params[key][0].data[...] = wt
                nobn.params[key][1].data[...] = bias


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pycaffe', type=str, default=DIR_PYCAFFE, help='pycaffe path')
    parser.add_argument('--model', type=str, required=True, help='.prototxt file for inference')
    parser.add_argument('--weights', type=str, required=True, help='.caffemodel file for inference')
    parser.add_argument('--model_out', type=str, default='no_bn.prototxt', help='output prototxt file path')
    parser.add_argument('--weights_out', type=str, default='no_bn.caffemodel', help='output weights file path')
    args = parser.parse_args()

    ## check input args
    if not os.path.exists(args.model):
        sys.exit("proto file not found:", args.model)
    if not os.path.exists(args.weights):
        sys.exit("caffe model not found:", args.weights)

    sys.path.append(args.pycaffe)
    print(args.pycaffe)
    try:
        import caffe
    except ImportError:
        sys.exit("Import caffe failed!")

    ## update old model proto file
    pre_process(args.model, args.model_out)

    ## create old model with weights
    net = caffe.Net(args.model, args.weights, caffe.TEST)
    ## create new model with empty weights
    net2 = caffe.Net(args.model_out, caffe.TEST)
    ## load weights from origin model
    load_weights(net, net2)
    ## save new weights to disk
    net2.save(args.weights_out)
