import torch
import os
import folder_paths

from ..client_s3 import get_s3_instance
S3_INSTANCE = get_s3_instance()

class IPAdapterSaveFaceIdS3:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "faceid": ("FACEID",),
            "filename": ("STRING", {"default": "FaceID"})
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "ipadapter/faceid"

    def save(self, faceid, filename):
        local_path = file = os.path.join(folder_paths.get_output_directory(), filename)
        torch.save(faceid, local_path)
        s3_path = os.path.join(os.getenv("S3_OUTPUT_DIR"), filename)
        S3_INSTANCE.upload_file(local_path=local_path, s3_path=s3_path)
        return (None, )


class IPAdapterLoadFaceIdS3:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"faceid": ("STRING", {"default": "PathToFaceID"}) } }

    RETURN_TYPES = ("FACEID", )
    FUNCTION = "load"
    CATEGORY = "ipadapter/faceid"

    def load(self, faceid):
        input_dir = folder_paths.get_input_directory()
        local_path = os.path.join(input_dir, faceid)
        s3_path = os.path.join(os.getenv("S3_INPUT_DIR"), faceid)
        downloaded_path = S3_INSTANCE.download_file(s3_path=s3_path, local_path=local_path)
        faceid = torch.load(downloaded_path)
        return ({ "cond": faceid["cond"] , "uncond": faceid["uncond"], "cond_alt" : faceid["cond_alt"], "img_cond_embeds": faceid["img_cond_embeds"]}, )
