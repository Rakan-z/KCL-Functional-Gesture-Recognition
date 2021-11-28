# KCL-Functional-Gesture-Recognition
This repository consists of files which include the thesis report and MATLAB programs for my BEng Final Year Individual Project. Each file is described in the below sections.
- Grade: 73/100 --- Award: First Class Honours/Pass with Distinction. 
- Topic description: This project investigates the application of gesture recognition in the context of a surgical operating room where touchless interface is paramount to maintaining sterility. This project proposes a new method of building such systems, using Google’s newly released MediaPipe framework to do so. A model has been built and tested with promising results. 
- Project Demonstration (powerpoint presentation): https://emckclac-my.sharepoint.com/:p:/g/personal/k1764173_kcl_ac_uk/ETzzTfrfVnRHi0qzlL8oQd8BecgzOIAsE5LbheF1HrNGiQ?e=rb4JbB

Thesis.pdf
-
The project report (thesis paper).

FBS_Boundary_search_lin.m
-
The program which includes the algorithm that linearly clusters the GNs.

FBS_Boundary_search_pw.m
-
The program which includes the algorithm that clusters the GNs using a Piecewise defined function.

READMEthesisFinal.md
-
A guide to the project files.

Simulation_linear_crowd.m
-
The program which simulates a multi-cell environment with a flashcrowd and uses the FBS_Boundary_search_lin algorithm to plan the FBS routes.

Simulation_linear.m
-
The program which simulates a multi-cell environment and uses the FBS_Boundary_search_lin algorithm to plan the FBS routes.

Simulation_piecewise_crowd.m
-
The program which simulates a multi-cell environment with a flashcrowd and uses the FBS_Boundary_search_pw algorithm to plan the FBS routes.

Simulation_piecewise.m
-
The program which simulates a multi-cell environment and uses the FBS_Boundary_search_pw algorithm to plan the FBS routes.

tspsearch.m
-
The 2-opt algorithm used to build the clustering algorithms.

