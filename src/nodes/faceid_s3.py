import torch
import os
import folder_paths
import tempfile
import time

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
        start_time = time.time()  # Record the start time

        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".faceid") as temp_file:
                temp_file_path = temp_file.name

                # Save faceid to temp file
                torch.save(faceid, temp_file_path)

                # Upload the temporary file to S3
                s3_path = os.path.join(os.getenv("S3_OUTPUT_DIR"), filename)
                S3_INSTANCE.upload_file(temp_file_path, s3_path)

        finally:
            # Delete the temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        end_time = time.time()  # Record the end time
        print("### Saved faceId in: {:.6f} seconds".format(end_time - start_time))

        return (None, )


class IPAdapterLoadFaceIdS3:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"faceid": ("STRING", {"default": "PathToFaceID"}) } }

    RETURN_TYPES = ("FACEID", )
    FUNCTION = "load"
    CATEGORY = "ipadapter/faceid"

    def load(self, faceid):
        start_time = time.time()  # Record the start time

        input_dir = folder_paths.get_input_directory()
        local_path = os.path.join(input_dir, faceid)
        if not os.path.exists(local_path):
            print("### downloading faceid file")
            s3_path = os.path.join(os.getenv("S3_INPUT_DIR"), faceid)
            local_path = S3_INSTANCE.download_file(s3_path=s3_path, local_path=local_path)
        else:
            print("### using cached faceid file")
        faceid = torch.load(local_path)

        end_time = time.time()  # Record the end time
        print("### Loaded faceId in: {:.6f} seconds".format(end_time - start_time))

        return ({ "cond": faceid["cond"] , "uncond": faceid["uncond"], "cond_alt" : faceid["cond_alt"], "img_cond_embeds": faceid["img_cond_embeds"]}, )





class IPAdapterSaveEmbedsS3:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(s):
        return {"required": {
            "embeds": ("EMBEDS",),
            "filename": ("STRING", {"default": "Embeds"})
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save"
    OUTPUT_NODE = True
    CATEGORY = "ipadapter/faceid"

    def save(self, embeds, filename):
        start_time = time.time()  # Record the start time

        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".embeds") as temp_file:
                temp_file_path = temp_file.name

                # Save faceid to temp file
                torch.save(embeds, temp_file_path)

                # Upload the temporary file to S3
                s3_path = os.path.join(os.getenv("S3_OUTPUT_DIR"), filename)
                S3_INSTANCE.upload_file(temp_file_path, s3_path)

        finally:
            # Delete the temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

        end_time = time.time()  # Record the end time
        print("### Saved faceId in: {:.6f} seconds".format(end_time - start_time))

        return (None, )


class IPAdapterLoadEmbedsS3:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"embeds": ("STRING", {"default": "PathToEmbeds"}) } }

    RETURN_TYPES = ("EMBEDS", )
    FUNCTION = "load"
    CATEGORY = "ipadapter/faceid"

    def load(self, embeds):
        start_time = time.time()  # Record the start time

        input_dir = folder_paths.get_input_directory()
        local_path = os.path.join(input_dir, faceid)
        if not os.path.exists(local_path):
            print("### downloading faceid file")
            s3_path = os.path.join(os.getenv("S3_INPUT_DIR"), faceid)
            local_path = S3_INSTANCE.download_file(s3_path=s3_path, local_path=local_path)
        else:
            print("### using cached faceid file")
        faceid = torch.load(local_path)

        end_time = time.time()  # Record the end time
        print("### Loaded faceId in: {:.6f} seconds".format(end_time - start_time))

        return ({ "cond": embeds["cond"] , "uncond": embeds["uncond"], "cond_alt" : embeds["cond_alt"], , "img_cond_embeds" : embeds["img_cond_embeds"]}, )
