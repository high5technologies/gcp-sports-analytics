
resource "google_bigquery_table" "bq_table_nba_raw_nbacom_game" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_nbacom_game"
    schema = file("${path.module}/bigquery/tables/nba_raw_nbacom_game.json")
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "nba"
    }
    time_partitioning  {                       
        type                     = "DAY"
        field                    = "game_date"
        require_partition_filter = false
        expiration_ms            = null   
    }
    deletion_protection = true
}

resource "google_bigquery_table" "bq_table_nba_raw_nbacom_game_player" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_nbacom_game_player"
    schema = file("${path.module}/bigquery/tables/nba_raw_nbacom_game_player.json")
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "nba"
    }
    time_partitioning  {                       
        type                     = "DAY"
        field                    = "game_date"
        require_partition_filter = false
        expiration_ms            = null   
    }
    deletion_protection = true
}

resource "google_bigquery_table" "bq_table_nba_raw_nbacom_game_inactive" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_nbacom_game_inactive"
    schema = file("${path.module}/bigquery/tables/nba_raw_nbacom_game_inactive.json")
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "nba"
    }
    time_partitioning  {                       
        type                     = "DAY"
        field                    = "game_date"
        require_partition_filter = false
        expiration_ms            = null   
    }
    deletion_protection = true
}

resource "google_bigquery_table" "bq_table_nba_raw_nbacom_game_official" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_nbacom_game_official"
    schema = file("${path.module}/bigquery/tables/nba_raw_nbacom_game_official.json")
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "nba"
    }
    time_partitioning  {                       
        type                     = "DAY"
        field                    = "game_date"
        require_partition_filter = false
        expiration_ms            = null   
    }
    deletion_protection = true
}

resource "google_bigquery_table" "bq_table_nba_raw_nbacom_game_team_period_score" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_nbacom_game_team_period_score"
    schema = file("${path.module}/bigquery/tables/nba_raw_nbacom_game_team_period_score.json")
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "nba"
    }
    time_partitioning  {                       
        type                     = "DAY"
        field                    = "game_date"
        require_partition_filter = false
        expiration_ms            = null   
    }
    deletion_protection = true
}

resource "google_bigquery_table" "bq_table_nba_raw_nbacom_game_event" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_nbacom_game_event"
    schema = file("${path.module}/bigquery/tables/nba_raw_nbacom_game_event.json")
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "nba"
    }
    time_partitioning  {                       
        type                     = "DAY"
        field                    = "game_date"
        require_partition_filter = false
        expiration_ms            = null   
    }
    deletion_protection = true
}

