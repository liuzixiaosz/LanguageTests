while ((1))
do
    echo "please input:"
    read string
    echo "replacing $string with *$string*..."
    sed -ig "s/$string/*$string*/g" ./Words/Words.md
    sed -ig "s/$string/*$string*/g" ./Words/WordsCopy.md
    echo "OK"
done