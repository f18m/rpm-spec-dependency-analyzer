#!/usr/bin/python3

#
# Purpose: Read SPEC files and generate a .DOT file that describes dependencies among them.
#          IMPORTANT: requires Python3
# Author: fmontorsi
# Creation: June 2017
#


#from pyrpm.spec import Spec, replace_macros
from rpm_spec_dependency_analyzer.pyrpm_spec import *
import getopt, sys, os


##
## CONSTANTS
##

version_indicator=[ '=', '>=', '>', '<', '<=' ]



##
## FUNCTIONS
##

def before(value, a):
    """Find first part and return slice before it.
    """
    pos_a = value.find(a)
    if pos_a == -1: return ""
    return value[0:pos_a]

def clean_require_field( str ):
    """Removes SPEC-syntax stuff that DOT files don't like
    """
    for verind in version_indicator:
        if verind in str:
            str = before(str, verind)
            
    str = str.replace("(x86-32)","")
    str = str.replace("-","_")
    str = str.replace("(","")
    str = str.replace(")","")
    str = str.replace(".","")
    str = str.replace(",","")
    str = str.replace("%{","")
    str = str.replace("}","")
    return str.strip()

def build_requirements_digraph( spec ):
    """Parses given RPM spec file and generates a list in the form
         [
           [ a, b ]
           [ b, c ]
           ...
         ]
       indicating that RPM "a" depends from RPM "b". RPM "b" depends from "c" etc.
    """
    
    all_cleaned_reqs = []
    all_req = spec.requires
    all_req.extend( spec.requires_post)
    for req in all_req:
        cleaned_req = []
        for pkgname in str(req).split(','):
            cleaned_req.append(clean_require_field(pkgname))
        #print('req tranformed [{}] -> [{}]'.format(req, cleaned_req))
        all_cleaned_reqs = all_cleaned_reqs + cleaned_req

    #print('All requirements are: {}'.format(all_cleaned_reqs))
    output_digraph = []
    for req in all_cleaned_reqs:
        output_digraph.append([ clean_require_field(spec.name), req ])
    return output_digraph


def build_node_labels( spec ):
    """Parses given RPM spec file and generates a list in the form
         [
           [ a, LABEL, SHAPE, COLOUR ]
           [ b, LABEL, SHAPE, COLOUR ]
           ...
         ]
       associating each RPM with its LABEL
    """
    nodename = clean_require_field(spec.name)
    #print(spec.name, nodename)
    if len(spec.files) == 0:
        return [ nodename, nodename + "\\nMETA PACKAGE", "box", "darkolivegreen4" ]
    return [ nodename, nodename, "ellipse", "deepskyblue1" ]

def process_specs( specfiles ):
    """Processes a list of RPM spec files
    """
    
    output_nodes = []
    output_digraph = []
    for specfilename in specfiles:
        print('Processing spec file: ' + specfilename)
        spec = Spec.from_file(specfilename)
        nodelist = build_node_labels(spec)
        reqlist = build_requirements_digraph(spec)

        output_nodes.append(nodelist)
        output_digraph.extend(reqlist)
        print(' ...found {} requirements, {} files.'.format(len(reqlist), len(spec.files)))

    return {'output_digraph': output_digraph, 
            'output_nodes' : output_nodes }

def generate_dot_file(outputfile, dict_graph):
    """Taking a digraph structure writes a .dot file that can be processed by "dot" utility
    """
    print('Generating DOT file: {}'.format(outputfile))
    of = open(outputfile,'w')
    of.write("digraph Dependencies {\n")
    for pair in dict_graph['output_nodes']:
        of.write('{} [shape={} style="filled" fillcolor={} label="{}"]\n'.format(pair[0], pair[2], pair[3], pair[1]))
    for pair in dict_graph['output_digraph']:
        of.write( pair[0] + " -> " + pair[1] + "\n" )
    of.write("}\n")
        
def usage():
    """Provides commandline usage
    """
    print('Usage: %s [--help] --output=somefile.dot <spec files> ...' % sys.argv[0])
    print('  [-h] --help                 (this help)')
    print('  [-o] --output=<filename>    Output file for Graphviz dot utility (https://www.graphviz.org/);')
    print('                              the graph represents the dependencies among the .spec files')
    print('  <spec files> ...            List of .spec files to analyze')
    sys.exit(0)
    
def parse_command_line():
    """Parses the command line
    """
    try:
        opts, remaining_args = getopt.getopt(sys.argv[1:], "ho", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()

    outputdot = ""
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-o", "--output"):
            outputdot = a
        else:
            assert False, "unhandled option"

    if outputdot == "":
        print("Please provide --output option")
        sys.exit(os.EX_USAGE)

    return {'spec_files': remaining_args, 
            'outputdot' : outputdot }

##
## MAIN
##

def main():
    config = parse_command_line()
    output = process_specs(config['spec_files'])
    generate_dot_file(config['outputdot'], output)

if __name__ == '__main__':
    main()
