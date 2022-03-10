# importing libraries
import cv2
import os

# Importing function to resize images
from app.service.helper.image_resizer import image_resize

# Filtering Warnings
import warnings
warnings.filterwarnings('ignore')

# finding path of application's root folder
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = APP_ROOT[:-15]

from detectron2.utils.logger import setup_logger
setup_logger()
setup_logger(name="mask2former")

# importing some common detectron2 utilities
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.projects.deeplab import add_deeplab_config
coco_metadata = MetadataCatalog.get("coco_2017_val_panoptic")

# Configurations to use pre-trained model
from app.resource.Model.Mask2Former.mask2former import add_maskformer2_config
cfg = get_cfg()
add_deeplab_config(cfg)
add_maskformer2_config(cfg)
cfg.merge_from_file(APP_ROOT+"/resource/Model/Mask2Former/configs/coco/panoptic-segmentation/swin/maskformer2_swin_large_IN21k_384_bs16_100ep.yaml")
cfg.MODEL.WEIGHTS = APP_ROOT+"/resource/Model/Mask2Former/PretrainedModel/model_final_f07440.pkl"
cfg.MODEL.MASK_FORMER.TEST.PANOPTIC_ON = True  # we are using panoptic segmentation

# Initializing predictor object
predictor = DefaultPredictor(cfg)

# renaming category names which contains 'other', 'merged' and 'other-merged'
all = coco_metadata.stuff_classes
for i in range(len(all)):
    if '-other-merged' in all[i]:
        all[i] = all[i][:-13]
    elif '-merged' in all[i]:
        all[i]=all[i][:-7]
    elif '-other' in all[i]:
        all[i]=all[i][:-6]
coco_metadata.stuff_classes = all  # updating category names with renamed names

# Class for panoptic segmentation
class ObjDetection:
    def predict(self, image_path):
        img = cv2.imread(image_path)
        img_resized = image_resize(img) # resizing image
        outputs = predictor(img_resized) # using predictor object of model

        detected = [] # it will contain objects detected in image
        for i in outputs["panoptic_seg"][1]:
            obj = coco_metadata.stuff_classes[i['category_id']]
            if obj not in detected:
                detected.append(obj)

        return detected
