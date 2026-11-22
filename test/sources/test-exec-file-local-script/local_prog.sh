# Code that reproduce a user's program to be used in our tests."""

output_file="<data.csv>"

echo '"Treat", "Quantity", "Description"' > $output_file
echo '"Albatross", 2.99, "On a stick!"' >> $output_file
echo '"Crunchy Frog", 1.49, "If we took the bones out,' >> $output_file
echo "it wouldn't be crunchy, now would it?"'"' >> $output_file
echo '"Gannet Ripple", 1.99, "On a stick!"' >> $output_file
