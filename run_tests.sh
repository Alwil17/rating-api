#!/bin/bash
export TESTING=True
export PYTHONPATH=$PYTHONPATH:$(pwd)
pytest $@
