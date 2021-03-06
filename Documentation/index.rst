.. SeisSol documentation master file, created by
   sphinx-quickstart on Wed Nov  7 15:42:26 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=======
SeisSol
=======

SeisSol is a software package for simulating wave propagation and dynamic
rupture based on the arbitrary high-order accurate derivative discontinuous
Galerkin method (ADER-DG).

Characteristics of the SeisSol simulation software are:

- use of tetrahedral meshes
- to approximate complex 3D model geometries and rapid model generation
- use of elastic, viscoelastic and viscoplastic material to approximate realistic geological subsurface properties
- use of arbitrarily high approximation order in time and space
- to produce reliable and sufficiently accurate synthetic seismograms or other seismological data set

.. toctree::
  :maxdepth: 2
  :caption: Introduction

  compilation
  a-first-example

.. toctree::
  :maxdepth: 2
  :caption: Structural models

  cad-models
  meshing-with-simmodeler
  meshing-with-pumgen
  gmsh

.. toctree::
  :maxdepth: 2
  :caption: Invoking SeisSol
  
  configuration
  parameter-file
  easi
  fault-tagging
  environment-variables

.. toctree::
  :maxdepth: 2
  :caption: Output
  
  fault-output
  free-surface-output
  off-fault-receivers
  postprocessing-and-visualization
  wave-field-output
  checkpointing

.. toctree::
  :maxdepth: 2
  :caption: Further documentation

  PUML-mesh-format
  asagi
  standard-rupture-format
  point-source-older-implementation
  dynamic-rupture
  computing-time-vs-order-of-accuracy
  performance-measurement
  attenuation
  2018-student-cluster-competition
  basic-code-structure
  known-issues

.. toctree::
  :maxdepth: 2
  :caption: Tutorials
  
  generating-a-cad-model-using-gocad-basic-tutorial
  remeshing-the-topography
  adapting-the-cad-model-resolution-using-gocad
  manually-fixing-an-intersection-in-gocad

.. toctree::
  :maxdepth: 2
  :caption: Unsorted

  meshing-partionning-with-pumgen-deprecated
  building-seissol-on-stampede-knl-test-system
  left-lateral-right-lateral-normal-reverse
  optimization-for-non-intel-architectures
