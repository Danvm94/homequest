INDEX=2
for file in *.jpg; do
    mv "$file" "$INDEX.jpg"
    ((INDEX++))
done

mogrify -format webp -define webp:target-size=200KB *.jpg

rm -rf *jpg