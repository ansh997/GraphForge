# GraphForge: Graph Reasoning over Language Models  

## Contributors  
- **Himanshu Pal** (IIIT-Hyderabad) - [himanshu.pal@research.iiit.ac.in](mailto:himanshu.pal@research.iiit.ac.in)  
- **Pranav Gupta** (IIIT-Hyderabad) - [pranav.gu@research.iiit.ac.in](mailto:pranav.gu@research.iiit.ac.in)  
- **Ananth Muppidi** (IIIT-Hyderabad) - [ananth.muppidi@students.iiit.ac.in](mailto:ananth.muppidi@students.iiit.ac.in)  

## Overview  
GraphForge explores how Large Language Models (LLMs) reason over graph-structured data. We investigate how different graph encoding methods impact LLM performance on various reasoning tasks and propose improvements for better structural understanding.  

## Key Findings  
- Graph encoding method significantly impacts LLM performance.  
- A new **Subprocess Order Encoding** improves reasoning over directed graphs.  
- **Island Encoding** enhances LLMs’ understanding of global graph structure.  
- Larger LLMs generally perform better, but Claude 3 outperforms GPT-4 on structural reasoning tasks.  

## Methods  
We evaluate multiple LLMs (GPT-4, Claude 3, Llama 3, Gemma 2B) using different node and edge encoding strategies:  
- **Node Encoding**: Integer, names (e.g., characters from South Park, politicians), alphabets.  
- **Edge Encoding**: Adjacency, co-authorship, social network descriptions, directional arrows.  
- **New Encodings**: Subprocess Order (for directed graphs), Island Encoding (global structure awareness).  

## Results  
- Subprocess Order consistently outperforms other encoding methods.  
- Island Encoding improves global structure understanding.  
- Performance improves with model size, but model-specific variations exist.  

## Citation  
If you use this work, please cite:  
```
@article{GraphForge2024,
  author    = {Himanshu Pal and Pranav Gupta and Ananth Muppidi},
  title     = {GraphForge: Graph Reasoning over Language Models},
  journal   = {Technical Report},
  year      = {2024},
  institution = {IIIT Hyderabad}
}
```


