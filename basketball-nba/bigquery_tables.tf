##########################################################################################
# Google BigQuery:  raw
##########################################################################################

resource "google_bigquery_table" "bq_table_nba_raw_nbastats_game" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_nbastats_game"
    schema = file("${path.module}/bigquery/tables/nba_raw_nbastats_game.json")
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


resource "google_bigquery_table" "bq_table_nba_raw_538_predictions" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_538_predictions"
    schema = file("${path.module}/bigquery/tables/nba_raw_538_predictions.json")
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "nba"
    }
    range_partitioning {
        field = "season"
        range {
            start = 1950
            end = 2100
            interval = 1
        }
    }
    deletion_protection = true
}

resource "google_bigquery_table" "bq_table_nba_raw_538_player_raptor" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_538_player_raptor"
    schema = file("${path.module}/bigquery/tables/nba_raw_538_player_raptor.json")
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "nba"
    }
    range_partitioning {
        field = "season"
        range {
            start = 1950
            end = 2100
            interval = 1
        }
    }
    deletion_protection = true
}

resource "google_bigquery_table" "bq_table_nba_raw_sbr_consensus" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_sbr_consensus"
    schema = file("${path.module}/bigquery/tables/nba_raw_sbr_consensus.json")
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

resource "google_bigquery_table" "bq_table_nba_raw_sbr_lines" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_sbr_lines"
    schema = file("${path.module}/bigquery/tables/nba_raw_sbr_lines.json")
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


resource "google_bigquery_table" "bq_table_nba_raw_basketballreference_game" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_basketballreference_game"
    schema = file("${path.module}/bigquery/tables/nba_raw_basketballreference_game.json")
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

resource "google_bigquery_table" "bq_table_nba_raw_basketballreference_playerbox" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_basketballreference_playerbox"
    schema = file("${path.module}/bigquery/tables/nba_raw_basketballreference_playerbox.json")
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


resource "google_bigquery_table" "bq_table_nba_raw_espn_predictions" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_espn_predictions"
    schema = file("${path.module}/bigquery/tables/nba_raw_espn_predictions.json")
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

resource "google_bigquery_table" "bq_table_nba_raw_espn_playbyplay" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_espn_playbyplay"
    schema = file("${path.module}/bigquery/tables/nba_raw_espn_playbyplay.json")
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
    clustering = ["game_date"]
    deletion_protection = true
}

resource "google_bigquery_table" "bq_table_nba_raw_swish_salary" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_swish_salary"
    schema = file("${path.module}/bigquery/tables/nba_raw_swish_salary.json")
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
    clustering = ["game_date"]
    deletion_protection = true
}

resource "google_bigquery_table" "bq_table_nba_raw_fantasylabs_ownership" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_fantasylabs_ownership"
    schema = file("${path.module}/bigquery/tables/nba_raw_fantasylabs_ownership.json")
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
    clustering = ["game_date"]
    deletion_protection = true
}

resource "google_bigquery_table" "bq_table_nba_raw_linestar_ownership" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "raw_linestar_ownership"
    schema = file("${path.module}/bigquery/tables/nba_raw_linestar_ownership.json")
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
    clustering = ["game_date"]
    deletion_protection = true
}

##########################################################################################
# Google BigQuery:  reference
##########################################################################################

resource "google_bigquery_table" "nba_ref_team" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "ref_team"
    description = "google sheet that provides meta data to basketball reference provides.  Google sheet is manually maintained.  This table should be used in LEFT JOINs to prevent data loss if data does not exist in google sheet reference values"
    schema = file("${path.module}/bigquery/tables/nba_ref_team.json")
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "nba"
    }
    external_data_configuration {
        autodetect    = false
        source_format = "GOOGLE_SHEETS"

        google_sheets_options {
            skip_leading_rows = 1
            range = "reference!A:F"
        }

        source_uris = [
            "https://docs.google.com/spreadsheets/d/1nHPWY-017onYBgtC7E_enqmCLDi-oCnr5cyHk8enPYM/"
        ]
    }
    deletion_protection = true
}

resource "google_bigquery_table" "nba_ref_538_spread_probability" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "ref_538_spread_probability"
    description = "google sheet on historical data for the 538 probability to spread"
    schema = file("${path.module}/bigquery/tables/nba_ref_538_spread_probability.json")
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "nba"
    }
    external_data_configuration {
        autodetect    = false
        source_format = "GOOGLE_SHEETS"

        google_sheets_options {
            skip_leading_rows = 1
            range = "prob!A:B"
        }

        source_uris = [
            "https://docs.google.com/spreadsheets/d/1MA0MExULs2K826hq6ICseargZMMU6CbrMi_1JHRjtPU/"
        ]
    }
    deletion_protection = true
}



resource "google_bigquery_table" "nba_ref_team_alias" {
    dataset_id = google_bigquery_dataset.bq_dataset_nba.dataset_id
    table_id   = "ref_team_alias"
    description = "google sheet that provides aliases for different source systems that have may different team aliases in their data sets.  Google sheet is manually maintained.  This table should be used in LEFT JOINs to prevent data loss if data does not exist in google sheet reference values"
    schema = file("${path.module}/bigquery/tables/nba_ref_team_alias.json")
    labels = {
        env = var.env
        project = "sports_analytics"
        league = "nba"
    }
    external_data_configuration {
        autodetect    = false
        source_format = "GOOGLE_SHEETS"

        google_sheets_options {
            skip_leading_rows = 1
            range = "alias!A:B"
        }

        source_uris = [
            "https://docs.google.com/spreadsheets/d/1nHPWY-017onYBgtC7E_enqmCLDi-oCnr5cyHk8enPYM/"
        ]
    }
    deletion_protection = true
}