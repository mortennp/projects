cd ~/Documents/GitHub
git clone https://github.com/pjreddie/darknet
cd darknet
make OPENMP=1 -j 2
mkdir weights
cd weights
wget https://pjreddie.com/media/files/yolov3-tiny.weights 
cd ..
./darknet detect cfg/yolov3-tiny.cfg weights/yolov3-tiny.weights data/dog.jpg