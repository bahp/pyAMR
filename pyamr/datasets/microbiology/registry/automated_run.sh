# ------------------------------
# Create Microorganisms Registry
# ------------------------------
# Create gram_stain database
cd microorganisms/gram_stain/
python script.py

# Create taxonomy database
cd ../../
cd microorganisms/taxonomy/
python script.py

# Create microorganism registry
cd ../../
cd microorganisms/
python script.py

# ------------------------------
# Create Antimicrobials Registry
# ------------------------------
# Create categories database
cd ../
cd antimicrobials/categories/
python script.py

# Create antimicrobials registry
cd ../../
cd antimicrobials/
python script.py

$SHELL
