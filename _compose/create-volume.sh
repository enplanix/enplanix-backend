VOLUMES=("postgres_data" "static_data")

for volume in "${VOLUMES[@]}"; do
    if ! docker volume inspect "$volume" >/dev/null 2>&1; then
        echo "Creating volume: $volume"
        docker volume create "$volume"
    else
        echo "Volume already exists: $volume"
    fi
done
