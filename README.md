# [MedlinePlus](https://medlineplus.gov/)
> MedlinePlus is a service of the National Library of Medicine (NLM), the world's largest medical library, which is part of the National Institutes of Health (NIH).


## MedlinePlus is the New Home of *Genetics Home Reference*
> **Genetics Home Reference** is now part of **MedlinePlus**, an online health information resource from the National Library of Medicine (NLM).
> Information from the Genetics Home Reference website is available in a new section called ***MedlinePlus Genetics***.

## Dependencies
- Python3.6+


## Installation
```bash
pip3 install medlineplus
```

## Usage
```
medlineplus

medlineplus gene -l -s a
medlineplus gene -s a -o a.gene
medlineplus gene -s a -o a.gene -O xml

medlineplus condition -l -s b
medlineplus condition -s b -o b.condition
medlineplus condition -s b -o b.condition -O xml
```

## Examples
- [GHR.gene.jl](https://suqingdong.github.io/medlineplus/examples/GHR.gene.jl)
- [GHR.condition.jl](https://suqingdong.github.io/medlineplus/examples/GHR.condition.jl)
- [z.gene.xml](https://suqingdong.github.io/medlineplus/examples/z.gene.xml)
- [z.condition.xml](https://suqingdong.github.io/medlineplus/examples/z.condition.xml)
