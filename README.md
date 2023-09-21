# 3DVision-Multi-level-3D-Scene-Graph

1. First shoot an MP4 video and split it into JPG/PNG images with 30 FPS.

2. Extract SRT file from MP4 video using an online platform like EasySub.
Save the SRT file.

3. Use the edit_srt.py script to clean the SRT file.

4. Use the mp4-to-srt.py script to create an image to keyword mapping CSV file.
OR Use the video-image-srt-mapping.py script to create an excel sheet mapping.

5. Download the OVSeg pipeline from: https://github.com/facebookresearch/ov-seg.git.

6. Create an Anaconda environment using the ovseg_env.yml file.
Install OVseg within this pipeline. Download the pre-trained ViT model as described on OVSeg GitHub.

7. Copy original images to the OVSeg folder. 

8. Copy the run_ovseg.py script to OVSeg root folder.

9. Copy the predictor.py to ov-seg/open_vocab_seg/utils. Change alpha value to 0.5 for transparent masks or to 1 for opaque masks.

10. Run demo.py or run_ovseg.py with the correct path to the configuration file and the model weights. Wait up to 4-12 hours depending on your computing setup for about 9000 images.

11. Use transparent masked images for COLMAP reconstruction.
Use opaque masked images for back projection.

12. From COLMAP reconstruction, feed the images, select SIMPLE_RADIAL, Shared for all images and estimate_affine_shape for feature extraction.
Select guided matching for sequential feature matching. Run the reconstruction.

13. After obtaining the final points3D.txt, manually segment it using CloudCompare and desired colours to generate ground truth.
Output ASC file for each label and also for the final fused ground truth point cloud.

14. Use add-labels-asc.py script to add labels to the ground truth point cloud.

15. Use clean-3D-points.py to clean the computationally segmented or backprojected points3D.txt

16. Use label-3D-points.py to label the computationally segmented or backprojected points3D.txt

17. Use compute-IoU.py to compute the IoU with the ground truth point cloud. One label at a time.

18. Use compute_IoU-Error.py first and Update-CSV.py to find the number of missed points in semantic segmentation and IoU computation due to cosine similarity threshold. 

Check IoU Error Analysis excel sheets for reference
