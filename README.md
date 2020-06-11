# Beyond Worst Case Analysis of Budget Feasible Mechanisms

This repository is the official implementation of Beyond Worst Case Analysis of Budget Feasible Mechanisms. 

## Requirements

- Environment: Python 3.8.3 and Mathematica 12.0.0.0
- To install requirements for Python:
    ```
    pip install numpy
    ```

> 📋The numerical simulation for Table 1 in the main paper is implemented in Mathematica 12. The experiments for Table 2, 3, 4 and Figure 2 in the main paper and Figure 3 in the supplementary material are implemented in Python 3.8.3 with numpy 1.18.4. 

## Evaluation
- To generate results of Table 1 in the main paper, run the following files separately in Mathematica (running file row_i.nb generates the result of i-th row of Table 1):

    ```
    row_1.nb, row_2.nb, row_3.nb, row_4.nb
    ```

- To generate Figure 3 in the supplementary material, run ```figure_3.nb``` in Mathematica.

- To generate results of Table 2, 3, 4 in the main paper, run:

    ```
    python procurement.py 1
    ```

- To generate results of Figure 2 in the main paper, run:

    ```
    python procurement.py 2
    ```

## Results
- Running Mathematica file ```row_i.nb``` would output a single number that corresponds to the number recorded in the i-th row of Table 1 in the main paper.

- Running ```figure_3.nb``` in Mathematica generates Figure 3 in the supplementary material.

- Running command
    ```
    python procurement.py 1
    ```
    would generate two files ```output_table_2_3_4.txt``` and ```log_table_2_3_4.txt```. ```output_table_2_3_4.txt``` contains the results recorded in Table 2, 3, 4, and ```log_table_2_3_4.txt``` contains the detail results of every single run of the experiment (there are 100 runs in total).

    ```output_table_2_3_4.txt``` consists of 5 chunks, for example, each chunk looks like the following:
    ```
    distribution: 0, mean_apx_cutoff: 0.8164167743343413, std_apx_cutoff: 0.003994976553218549, mean_apx_agn: 0.6328363161492855, std_apx_agn: 0.0011647696910553067, mean_apx_greedy: 0.8180859364491048, std_apx_greedy: 0.0036981733764886227, mean_apx_random: 0.8107890395127277, std_apx_random: 0.005572663823142807
    distribution: 0, mean_welfare_cutoff: 4994.514281712639, std_welfare_cutoff: 112.85372385794611, mean_welfare_agn: 7889.67903118912, std_welfare_agn: 56.054533364295466, mean_welfare_greedy: 4982.622237302562, std_welfare_greedy: 105.65100866076922, mean_welfare_random: 4945.228777100618, std_welfare_random: 102.32825734010231
    distribution: 0, mean_efficiency_cutoff: 0.05437334855482678, std_efficiency_cutoff: 0.0004141435424286287, mean_efficiency_agn: 0.05221194648349061, std_efficiency_agn: 0.0004265994118420018, mean_efficiency_greedy: 0.054364002154696056, std_efficiency_greedy: 0.00041067817849718447, mean_efficiency_random: 0.054473337521224616, std_efficiency_random: 0.0004186358811788315
    ```
    in which ''distribution: i-1'' means this result corresponds to i-th row of Table 2, 3, 4 in the main paper, specifically, the first line outputs the results of Table 2, and the second line outputs the result of Table 3, and the third line outputs the results of Table 4.

- Running command
    ```
    python procurement.py 2
    ```
    would generate two files ```output_figure_2.txt``` and ```log_figure_2.txt```. ```output_figure_2.txt``` contains the results recorded in Figure 2 of the main paper, and ```log_figure_2.txt``` contains the detailed results of every single run of the experiment (there are 20 runs in total).

    ```output_figure_2.txt``` consists of 5 chunks, for example, each chunk looks like the following:
    ```
    distribution: 0, mean diff: 0.02925263496368514, std diff: 0.011923399650247146, mean apx greedy: 0.8290048079775515, std apx greedy: 0.012594671371202263, mean apx random: 0.799752173013866, std apx random: 0.019057321857692926, number of sellers: 100
    distribution: 1, mean diff: 0.03845175264199979, std diff: 0.012522087392968935, mean apx greedy: 0.7256426672434181, std apx greedy: 0.0133416948264606, mean apx random: 0.6871909146014182, std apx random: 0.018814813174914683, number of sellers: 100
    distribution: 2, mean diff: 0.024299699130186043, std diff: 0.015229319555741899, mean apx greedy: 0.7526601739043456, std apx greedy: 0.024893128151607068, mean apx random: 0.7283604747741595, std apx random: 0.034790306225640166, number of sellers: 100
    ```
    in which ''distribution: i-1'' means this result corresponds to i-th sub-figure of Figure 2, and each line corresponds to one datapoint in a sub-figure, for example, in the first line, ''distribution'' is ''0'', and the last item ''number of sellers'' is ''100'', hence, this corresponds to the datapoint whose x-axis value is 100 in the first sub-figure of Figure 2, and moreover, ''mean diff'' corresponds to the y-axis value of this datapoint, and ''std diff'' corresponds to one standard deviation of the y-axis value of this datapoint (this is captured by the shaded area in this sub-figure).

- To generate the sub-figures, for example, one can use the following snippet in Mathematica:
    ```
    gaussian = {{100, 
        Around[0.02925263496368514, 0.011923399650247146]}, {300, 
        Around[0.014817959068239284, 0.006705484781654666]}, {1000, 
        Around[0.007190387290917438, 0.0024568859917732224]}, {3000, 
        Around[0.003486243614250778, 0.0017771258363811781]}, {10000, 
        Around[0.0018644748969711025, 0.0006882971788771211]}};
    uniform = {{100, 
        Around[0.03845175264199979, 0.012522087392968935]}, {300, 
        Around[0.02214898154479154, 0.00869508451199778]}, {1000, 
        Around[0.00818787621654663, 0.004309654097105553]}, {3000, 
        Around[0.004622023759049543, 0.0018898286382246284]}, {10000, 
        Around[0.002074486786112789, 0.0008165122225426551]}};
    exponential = {{100, 
        Around[0.024299699130186043, 0.015229319555741899]}, {300, 
        Around[0.014498067400840175, 0.005397213417575599]}, {1000, 
        Around[0.006107502879750865, 0.0013825123552492658]}, {3000, 
        Around[0.002920768395526507, 0.0012584160230738974]}, {10000, 
        Around[0.0013225340913902484, 0.000549759167511513]}};
    subfig1 = ListLogLinearPlot[gaussian, IntervalMarkers -> "Bands", 
     IntervalMarkersStyle -> Pink, PlotMarkers -> Automatic, 
     AxesLabel -> {ToExpression["n", TeXForm, HoldForm], ""},  
     LabelStyle -> Directive[Black, 20], 
     Ticks -> {{100, 300, 1000, 3000, 10000}, Automatic}]
    subfig2 = ListLogLinearPlot[uniform, IntervalMarkers -> "Bands", 
     IntervalMarkersStyle -> Pink, PlotMarkers -> Automatic, 
     AxesLabel -> {ToExpression["n", TeXForm, HoldForm], ""},  
     LabelStyle -> Directive[Black, 20], 
     Ticks -> {{100, 300, 1000, 3000, 10000}, Automatic}]
    subfig3 = ListLogLinearPlot[exponential, IntervalMarkers -> "Bands", 
     IntervalMarkersStyle -> Pink, PlotMarkers -> Automatic, 
     AxesLabel -> {ToExpression["n", TeXForm, HoldForm], ""},  
     LabelStyle -> Directive[Black, 20], 
     Ticks -> {{100, 300, 1000, 3000, 10000}, Automatic}]
    ```

- For completeness, Table 1, 2, 3, 4 and Figure 2 of the main paper and Figure 3 of the supplementary material are presented below:

### [Table 1]
| Budget perturbation distribution | Worst-case approximation ratio |
| -------------------------------- | ------------------------------ |
|      Uniform over [1,10]         |            0.64                |
|   Log-scale-uniform over [1,8]   |            0.65                |
|   Log-scale-uniform over [1,512] |            0.67                |
|           Microworkers           |            0.64                |

### [Table 2]

|      CUTOFF      |       AGN        |     GREEDY-II    |    RS-GREEDY     |
| ---------------- | ---------------- | ---------------- | ---------------- |
| 0.816 +/-  0.004 | 0.632 +/-  0.001 | 0.818 +/-  0.004 | 0.810 +/-  0.006 |
| 0.709 +/-  0.005 | 0.633 +/-  0.003 | 0.711 +/-  0.004 | 0.702 +/-  0.006 |
| 0.740 +/-  0.008 | 0.663 +/-  0.006 | 0.743 +/-  0.008 | 0.736 +/-  0.009 |
| 0.690 +/-  0.003 | 0.633 +/-  0.002 | 0.726 +/-  0.003 | 0.718 +/-  0.005 |
| 0.680 +/-  0.009 | 0.634 +/-  0.003 | 0.712 +/-  0.006 | 0.706 +/-  0.007 |

### [Table 3]

|      CUTOFF      |       AGN        |     GREEDY-II    |    RS-GREEDY     |
| ---------------- | ---------------- | ---------------- | ---------------- |
|   4994 +/-  113  |   7889 +/-  56   |   4982 +/-  106  |   4945 +/-  102  |
|   9972 +/-  194  |  10131 +/-  143  |   9929 +/-  188  |   9861 +/-  188  |
|  12113 +/-  213  |  12654 +/-  135  |  12115 +/-  199  |  12049 +/-  193  |
|   9889 +/-  220  |   9617 +/-  124  |   8421 +/-  161  |   8363 +/-  154  |
|  11246 +/-  257  |  10611 +/-  162  |  10061 +/-  194  |  10013 +/-  195  |

### [Table 4]

|      CUTOFF       |       AGN         |     GREEDY-II     |     RS-GREEDY     |
| ----------------- | ----------------- | ----------------- | ----------------- |
| 0.054 +/-  0.0004 | 0.054 +/-  0.0004 | 0.054 +/-  0.0004 | 0.054 +/-  0.0004 |
| 0.071 +/-  0.002  | 0.064 +/-  0.001  |  0.07 +/-  0.002  | 0.071 +/-  0.002  |
| 0.094 +/-  0.002  |  0.09 +/-  0.002  | 0.094 +/-  0.002  | 0.095 +/-  0.002  |
| 0.068 +/-  0.002  |  0.06 +/-  0.001  | 0.062 +/-  0.001  | 0.062 +/-  0.001  |
| 0.078 +/-  0.002  | 0.067 +/-  0.002  | 0.071 +/-  0.002  | 0.072 +/-  0.002  |

### [Figure 2]
![N(20,5)](gaussian.png =100x)
![Unif(0,40)](uniform.png =100x)
![Exp(20)](exponential.png =100x)

### [Figure 3]
![2 budgets](2_budget.png =100x)

## Contributing

> 📋Please cite our paper Beyond Worst Case Analysis of Budget Feasible Mechanisms when you use the code or the results in this repository. Thanks!