
FOLDER_PATH="verified_sent/*"
for f in $FOLDER_PATH; 
    do 
        python3 generate_input_modularize_new.py $f > log.txt; 
    done
    