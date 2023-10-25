INDEX=56
for file in *.jpg; do
    mv "$file" "$INDEX.jpg"
    ((INDEX++))
done
mogrify -resize 600x400! *.jpg
mogrify -format webp -define webp:target-size=200KB *.jpg

rm -rf *jpg