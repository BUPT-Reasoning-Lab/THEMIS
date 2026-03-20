# Quick Start
## Installation
To handle the multimodal data efficiently, we recommend using the Hugging Face datasets library:
```bash
$ pip install -U "huggingface_hub[cli]"
```
## Loading the Data
You can load the dataset directly into your environment using the following snippet:
```bash
$ cd THEMIS_ROOT_DIR
$ huggingface-cli download BUPT-Reasoning-Lab/THEMIS --repo-type dataset --local-dir . --include "assets/dataset/*"
```
# Data Classification (Fraud Taxonomy)
The dataset is categorized based on the scope of the anomaly and the specific type of scientific fraud:

| Scope        | Fraud Type               | Level               | Fraud Type             | issue_id  |
|--------------|--------------------------|---------------------|------------------------|---------- |
| Intra-Element| Splicing                 | Panel               | Splicing               | FG_01     |
|              | Copy-move                | Panel               | Copy-move              | FG_02     |
|              | AI-generated             | Panel               | Image Inference Forgery| FG_03     |
|              |                          |                     | Targeted Region Editing| FG_04     |
| Inter-Element| Text--Image Inconsistency| Figure              | Numerical Inconsistency| TII_01    |
|              |                          |                     | Trend Inconsistency    | TII_02    |
|              | Duplication              | Panel               | Global                 | DUP_01    |       
|              |                          |                     | Local                  | DUP_02    |

## Directory Structure
The files are organized into the following directory structure to support modular access:
```
Dataset
├── forgery/                     
│   ├── ai_generated/            
│   │   ├── global                # Image Inference Forgery
│   │   └── partial               # Targeted Region Editing
│   ├── splicing                
│   ├── copy_move               
│   └── authentic                
├── duplication/                  
│   ├── global                 
│   ├── partial                 
│   └── authentic                
├── text_image_inconsistency/    
│   ├── numerical               
│   └── trend                    
└── retract/                      
```