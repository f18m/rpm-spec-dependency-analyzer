# rpm-spec-dependency-analyzer

This is a simple Python3 script that parses a list of SPEC files and
generates a nice graph of the dependencies among them using DOT.


## How to install

pip3 install python-rpm-spec
git clone https://github.com/f18m/rpm-spec-dependency-analyzer.git
cd rpm-spec-dependency-analyzer && ./specfiles_dependency_graph.py --output reqgraph.dot /my/spec/folder/*.spec
dot -Tpng reqgraph.dot reqgraph.png
