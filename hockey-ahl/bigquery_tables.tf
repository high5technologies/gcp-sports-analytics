
resource "google_bigquery_table" "bq_table_ahl_raw_hockeytech_roster" {
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id   = "raw_hockeytech_roster"
    schema = file("${path.module}/bigquery/tables/ahl_raw_hockeytech_roster.json")
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

resource "google_bigquery_table" "bq_view_ahl_vw_raw_hockeytech_game"{
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id = "vw_raw_hockeytech_game"
    depends_on = ["google_bigquery_table.bq_table_ahl_raw_hockeytech_game"]
    view {
        query = file("${path.module}/bigquery/views/vw_raw_hockeytech_game.sql")
        use_legacy_sql = false
    }
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
}

resource "google_bigquery_table" "bq_view_ahl_vw_raw_hockeytech_gamelog"{
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id = "vw_raw_hockeytech_gamelog"
    depends_on = ["google_bigquery_table.bq_table_ahl_raw_hockeytech_gamelog"]
    view {
        query = file("${path.module}/bigquery/views/vw_raw_hockeytech_gamelog.sql")
        use_legacy_sql = false
    }
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
}

resource "google_bigquery_table" "bq_view_ahl_vw_raw_hockeytech_coach"{
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id = "vw_raw_hockeytech_coach"
    depends_on = ["google_bigquery_table.bq_table_ahl_raw_hockeytech_coach"]
    view {
        query = file("${path.module}/bigquery/views/vw_raw_hockeytech_coach.sql")
        use_legacy_sql = false
    }
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
}

resource "google_bigquery_table" "bq_view_ahl_vw_raw_hockeytech_goaliebox"{
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id = "vw_raw_hockeytech_goaliebox"
    depends_on = ["google_bigquery_table.bq_table_ahl_raw_hockeytech_goaliebox"]
    view {
        query = file("${path.module}/bigquery/views/vw_raw_hockeytech_goaliebox.sql")
        use_legacy_sql = false
    }
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
}

resource "google_bigquery_table" "bq_view_ahl_vw_raw_hockeytech_goalielog"{
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id = "vw_raw_hockeytech_goalielog"
    depends_on = ["google_bigquery_table.bq_table_ahl_raw_hockeytech_goalielog"]
    view {
        query = file("${path.module}/bigquery/views/vw_raw_hockeytech_goalielog.sql")
        use_legacy_sql = false
    }
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
}

resource "google_bigquery_table" "bq_view_ahl_vw_raw_hockeytech_mvp"{
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id = "vw_raw_hockeytech_mvp"
    depends_on = ["google_bigquery_table.bq_table_ahl_raw_hockeytech_mvp"]
    view {
        query = file("${path.module}/bigquery/views/vw_raw_hockeytech_mvp.sql")
        use_legacy_sql = false
    }
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
}

resource "google_bigquery_table" "bq_view_ahl_vw_raw_hockeytech_ref"{
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id = "vw_raw_hockeytech_ref"
    depends_on = ["google_bigquery_table.bq_table_ahl_raw_hockeytech_ref"]
    view {
        query = file("${path.module}/bigquery/views/vw_raw_hockeytech_ref.sql")
        use_legacy_sql = false
    }
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
}

resource "google_bigquery_table" "bq_view_ahl_vw_raw_hockeytech_roster"{
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id = "vw_raw_hockeytech_roster"
    depends_on = ["google_bigquery_table.bq_table_ahl_raw_hockeytech_roster"]
    view {
        query = file("${path.module}/bigquery/views/vw_raw_hockeytech_roster.sql")
        use_legacy_sql = false
    }
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
}

resource "google_bigquery_table" "bq_view_ahl_vw_raw_hockeytech_skaterbox"{
    dataset_id = google_bigquery_dataset.bq_dataset_ahl.dataset_id
    table_id = "vw_raw_hockeytech_skaterbox"
    depends_on = ["google_bigquery_table.bq_table_ahl_raw_hockeytech_skaterbox"]
    view {
        query = file("${path.module}/bigquery/views/vw_raw_hockeytech_skaterbox.sql")
        use_legacy_sql = false
    }
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "ahl"
    }
}