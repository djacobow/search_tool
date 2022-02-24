import os, re, subprocess, binascii
from .. import util


class ProtobufDecode:
    def __init__(self, config):
        self.config = config

    def usage(self, adict):
        usage = []
        usage += [
            'pb -msg=<msgname> protobuf.in.hex.form',
            '',
            ' * msgname must be provided and must match something in cmt_messages.proto',
            ' * hex data can have spaces, dashes, whatever',
        ]
        return usage

    def run(self, adict):
       
        pb_text = re.sub(r'[^0-9a-fA-F]','',''.join(adict['args']))
        if not len(pb_text):
            util.die('provide a hex string')

        expected_message = adict.get('msg',None)
        if not expected_message:
            util.die('Provide the message type to decode with -msg=<msgname>')

        pb_bytes = binascii.unhexlify(pb_text)

        cmd = [
            'protoc --decode={}'.format(expected_message),
        ]

        cmd += [ '-I{}'.format(x) for x in self.config['commands']['pb']['searchpaths'] ]
        for protofile in self.config['commands']['pb']['protofiles']:
            cmd.append(protofile)
        cmds = ' '.join(cmd);
        p1 = subprocess.Popen(' '.join(cmd), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        out1 = p1.communicate(input=pb_bytes)
        print(out1[0].decode('utf-8'))
        


