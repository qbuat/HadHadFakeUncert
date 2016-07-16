#!/bin/bash

# function setup_rootcore()
# {
#     current_dir=${PWD}
#     cd ../packages ;source RootCore/scripts/setup.sh; cd ${current_dir}
# }
# setup_rootcore

SOURCE_HADHADFAKE_SETUP="${BASH_SOURCE[0]:-$0}"
DIR_HADHADFAKE_SETUP="$( dirname "$SOURCE_HADHADFAKE_SETUP" )"

while [ -h "$SOURCE_HADHADFAKE_SETUP" ]
do 
  SOURCE_HADHADFAKE_SETUP="$(readlink "$SOURCE_HADHADFAKE_SETUP")"
  [[ $SOURCE_HADHADFAKE_SETUP != /* ]] && SOURCE_HADHADFAKE_SETUP="$DIR_HADHADFAKE_SETUP/$SOURCE_HADHADFAKE_SETUP"
  DIR_HADHADFAKE_SETUP="$( cd -P "$( dirname "$SOURCE_HADHADFAKE_SETUP"  )" && pwd )"
  echo $SOURCE_HADHADFAKE_SETUP
  echo $DIR_HADHADFAKE_SETUP
done
DIR_HADHADFAKE_SETUP="$( cd -P "$( dirname "$SOURCE_HADHADFAKE_SETUP" )" && pwd )"

echo $DIR_HADHADFAKE_SETUP
echo "sourcing ${SOURCE_HADHADFAKE_SETUP}..."

export PATH=${DIR_HADHADFAKE_SETUP}${PATH:+:$PATH}
export PYTHONPATH=${DIR_HADHADFAKE_SETUP}${PYTHONPATH:+:$PYTHONPATH}
