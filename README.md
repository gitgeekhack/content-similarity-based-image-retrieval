# content-based-image-retrieval-poc-
**Python version :- 3.7.0**
### For runnig this project on CPU only device:
**Create python virtual environment using conda with specific version(3.7.0)** :-

	conda create -n "your_env_name" python=3.7.0

**Install PyTorch CPU only** :- 

    conda install pytorch torchvision torchaudio cpuonly -c pytorch

**Install Detectron2 CPU only** :-

    python -m pip install detectron2 -f \
    https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.10/index.html
  

**Additional libraries** :-
* libcudart.so.11.0
* libcudart.so.11.0.221
* libc10_cuda.so
* libcudart-80664282.so.10.2
* libgomp-a34b3233.so.1

**Put additional libraries into** - anaconda3/envs/your_env_name/lib/


