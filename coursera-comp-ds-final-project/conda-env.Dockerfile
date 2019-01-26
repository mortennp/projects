ARG ENV_NAME=comp-ds

# Start from a jupyter/docker-stacks image
FROM jupyter/minimal-notebook:87210526f381

# Install extensions into Jupyter (of base conda env)
RUN jupyter labextension install @pyviz/jupyterlab_pyviz \
 && fix-permissions $CONDA_DIR \
 && fix-permissions /home/$NB_USER

# Enable Jupyter (of base conda env) to use other conda envs
RUN conda install nb_conda_kernels

# Create comp-ds conda env from .yml file
COPY conda-environment.yml /tmp/
RUN conda env create -n comp-ds -f /tmp/conda-environment.yml \
 && fix-permissions $CONDA_DIR \
 && fix-permissions /home/$NB_USER

# Install extra conda packages that are not in .yml yet...
#RUN [ "/bin/bash", "-c", "source activate comp-ds && conda install ???" ]

# Install packages with pip (for packages not available through conda)
RUN [ "/bin/bash", "-c", "source activate comp-ds && pip install kaggle=='1.5.1'" ]

# Register custom env as kernel in base env's Jupyter
#RUN python -m ipykernel install --user --name=comp-ds --display-name "Python (comp-ds)"


