
resource "google_bigquery_table" "bq_table_ahl_raw_hockeytech_roster" {
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id   = "raw_hockeytech_roster"
    schema = file("${path.module}/bigquery/tables/ahl_raw_hockeytech_roster.json")
    deletion_protection=false
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
    range_partitioning {
        field = "season"
        range {
            start = 1950
            end = 2100
            interval = 1
        }
    }
}


resource "google_bigquery_table" "bq_table_ahl_raw_hockeytech_coach" {
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id   = "raw_hockeytech_coach" 
    schema = file("${path.module}/bigquery/tables/ahl_raw_hockeytech_coach.json")
    deletion_protection=false
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
    time_partitioning  {                       
        type                     = "DAY"
        field                    = "game_date"
        require_partition_filter = false
        expiration_ms            = null   
    }
}

resource "google_bigquery_table" "bq_table_ahl_raw_hockeytech_game" {
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id   = "raw_hockeytech_game" 
    schema = file("${path.module}/bigquery/tables/ahl_raw_hockeytech_game.json")
    deletion_protection=false
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
    time_partitioning  {                       
        type                     = "DAY"
        field                    = "game_date"
        require_partition_filter = false
        expiration_ms            = null   
    }
}



resource "google_bigquery_table" "bq_table_ahl_raw_hockeytech_gamelog" {
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id   = "raw_hockeytech_gamelog" 
    schema = file("${path.module}/bigquery/tables/ahl_raw_hockeytech_gamelog.json")
    deletion_protection=false
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
    time_partitioning  {                       
        type                     = "DAY"
        field                    = "game_date"
        require_partition_filter = false
        expiration_ms            = null   
    }
}

resource "google_bigquery_table" "bq_table_ahl_raw_hockeytech_goaliebox" {
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id   = "raw_hockeytech_goaliebox" 
    schema = file("${path.module}/bigquery/tables/ahl_raw_hockeytech_goaliebox.json")
    deletion_protection=false
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
    time_partitioning  {                       
        type                     = "DAY"
        field                    = "game_date"
        require_partition_filter = false
        expiration_ms            = null   
    }
}

resource "google_bigquery_table" "bq_table_ahl_raw_hockeytech_goalielog" {
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id   = "raw_hockeytech_goalielog" 
    schema = file("${path.module}/bigquery/tables/ahl_raw_hockeytech_goalielog.json")
    deletion_protection=false
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
    time_partitioning  {                       
        type                     = "DAY"
        field                    = "game_date"
        require_partition_filter = false
        expiration_ms            = null   
    }
}

resource "google_bigquery_table" "bq_table_ahl_raw_hockeytech_mvp" {
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id   = "raw_hockeytech_mvp" 
    schema = file("${path.module}/bigquery/tables/ahl_raw_hockeytech_mvp.json")
    deletion_protection=false
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
    time_partitioning  {                       
        type                     = "DAY"
        field                    = "game_date"
        require_partition_filter = false
        expiration_ms            = null   
    }
}

resource "google_bigquery_table" "bq_table_ahl_raw_hockeytech_ref" {
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id   = "raw_hockeytech_ref" 
    schema = file("${path.module}/bigquery/tables/ahl_raw_hockeytech_ref.json")
    deletion_protection=false
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
    time_partitioning  {                       
        type                     = "DAY"
        field                    = "game_date"
        require_partition_filter = false
        expiration_ms            = null   
    }
}

resource "google_bigquery_table" "bq_table_ahl_raw_hockeytech_skaterbox" {
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id   = "raw_hockeytech_skaterbox" 
    schema = file("${path.module}/bigquery/tables/ahl_raw_hockeytech_skaterbox.json")
    deletion_protection=false
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
    time_partitioning  {                       
        type                     = "DAY"
        field                    = "game_date"
        require_partition_filter = false
        expiration_ms            = null   
    }
}
