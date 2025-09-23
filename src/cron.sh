echo "Running on $(date)"

cd "$(dirname "$0")"

git checkout main
git pull

# weekly for weekly job
# monthly for monthly job
# test for test job
uv run -m kickball.main "$1"

cd ..
git add .
git commit -m "Weekly update"
git push
