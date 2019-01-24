# Start from a core stack version
FROM jupyter/minimal-notebook:87210526f381

# HDF5
RUN apt-get update && apt-get -yq dist-upgrade \
 && apt-get install -yq \
    libhdf5-dev

# Install PyViz extension into Jupyter
RUN jupyter labextension install @pyviz/jupyterlab_pyviz

# Install from requirements.txt file
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER