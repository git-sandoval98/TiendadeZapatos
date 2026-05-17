import os
import shutil

ia_dir = os.path.join(os.path.dirname(__file__), "ia")
if os.path.exists(ia_dir):
    shutil.rmtree(ia_dir)
    print("Deleted obsolete ia directory.")
