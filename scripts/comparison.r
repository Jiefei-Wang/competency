# 1. Install and Load packages
# install.packages("tidyverse")
library(tidyverse)

# 2. Load and prep LLM dataset
df <- read_csv("output/combined_tasks/combined_extraction_review.csv")

df_llm <- df |>
  rename_with(~ str_remove(., "_value"), contains("_value")) |>
  rename_with(~ paste0(., "_llm"), -cause_number)

# 3. Load and prep Jasper dataset
df_2 <- read_csv("output/jasper_dataset/jasper_extraction.csv")

df_jasper <- df_2 |>
  rename(
    currently_incarcerated = currently_incercerated,
    parents_married = patents_married,
    history_physical_abuse = hitstory_physical_abuse,
    manic_symptoms = manic_synptoms,
    prior_diagnosis = prior_diagnoses
  ) |>
  mutate(across(c(date_of_report, date_of_examination, evaluee_date_of_birth), 
                ~ as.Date(as.character(.), format = "%Y%m%d"))) |>
  mutate(across(c(age_of_first_use, number_of_competency_exams, number_of_times_found_incompetent, age_at_first_crime), as.numeric)) |>
  rename_with(~ paste0(., "_jasper"), -cause_number)

# 4. Merge them together into ONE dataset based on the patient name
target_files <- c("2017", "2019 (2)", "2019 (3)", "Abron, Michael (1962-05-09)", "AGUILAR,ERNESTO 02-04-1983")

df_combined <- inner_join(df_llm, df_jasper, by = "cause_number") |>
  filter(name_llm %in% target_files)

base_vars <- setdiff(names(df_llm), "cause_number") |> str_remove("_llm")

# Interleave the names 
interleaved_cols <- c("cause_number", as.vector(rbind(paste0(base_vars, "_llm"), paste0(base_vars, "_jasper"))))

df_combined <- df_combined |>
  select(any_of(interleaved_cols))

# Save the combined dataset for reference
write_csv(df_combined, "output/combined_tasks/llm_vs_jasper.csv")

# ---------------------------------------------------------
# NEW ANALYSIS FUNCTION (Simple Agreement)
# ---------------------------------------------------------

compare_agreement <- function(df, var_base) {
  llm_col <- paste0(var_base, "_llm")
  jasper_col <- paste0(var_base, "_jasper")
  
  # Skip if columns didn't merge properly
  if (!(llm_col %in% names(df)) || !(jasper_col %in% names(df))) {
    return(NULL)
  }
  
  # Force to character
  llm <- as.character(df[[llm_col]])
  jasper <- as.character(df[[jasper_col]])
  n_total <- length(llm)
  
  # Treat NA and empty cells as "unknown"
  llm[is.na(llm) | trimws(llm) == ""] <- "unknown"
  jasper[is.na(jasper) | trimws(jasper) == ""] <- "unknown"
  
  # Standardize for comparison
  llm_clean <- trimws(tolower(llm))
  jasper_clean <- trimws(tolower(jasper))
  
  # 1. Exact matches & Missing counts
  exact_matches <- sum(llm_clean == jasper_clean)
  llm_missing <- sum(llm_clean == "unknown")
  j_missing <- sum(jasper_clean == "unknown")
  agreement_pct <- (exact_matches / n_total) * 100
  
  # 2. Format output string: (4/5 matched, 80% agreement, LLM missing 2, J missing 2)
  summary_str <- sprintf("(%d/%d matched, %.0f%% agreement, LLM missing %d, J missing %d)", 
                         exact_matches, n_total, agreement_pct, llm_missing, j_missing)
  
  # 3. Capture vs. Accuracy Diagnosis (Check matches when BOTH have extracted data)
  both_present <- (llm_clean != "unknown") & (jasper_clean != "unknown")
  present_total <- sum(both_present)
  present_matches <- sum(llm_clean[both_present] == jasper_clean[both_present])
  
  capture_diagnosis <- if (present_total > 0) {
    if (present_matches == present_total) {
      sprintf("Perfect Match when extracted (%d/%d). Discrepancy is purely capture rate.", present_matches, present_total)
    } else {
      sprintf("Extraction discrepancy: %d/%d non-missing matched.", present_matches, present_total)
    }
  } else {
    "No overlapping extractions."
  }
  
  return(tibble(
    Variable = var_base,
    Summary_String = summary_str,
    Diagnosis_Notes = capture_diagnosis,
    Agreement_Pct = agreement_pct
  ))
}

# ---------------------------------------------------------
# VARIABLES & EXECUTION
# ---------------------------------------------------------

# Define all variables 
numeric_vars <- c(
  "court_number", "evaluee_age", "number_of_siblings", "number_of_suspensions",
  "number_of_expulsions", "longest_duration_of_employment", "total_marriages",
  "total_divorces", "number_of_children", "number_of_psychiatric_hospitalizations",
  "number_of_suicide_attempts", "age_of_first_use", "most_recent_use",
  "number_of_arrests", "number_of_incarcerations", "total_time_incarcerated",
  "number_of_prior_charges", "number_of_prior_convictions", 
  "number_of_times_found_incompetent", "age_at_first_crime"
)

categorical_vars <- c(
  "examiner", "date_of_report", "date_of_examination", "court_county",
  "evaluation_location", "facility_type", "currently_incarcerated",
  "examiner_qualifications", "evaluee_name", "evaluee_date_of_birth",
  "evaluee_sex", "evaluee_race", "current_charges", "offense_type",
  "family_history_mental_illness", "family_history_addiction",
  "family_history_suicide", "birthplace", "development_delays",
  "special_education", "parents_married", "parents_divorced",
  "parent_death", "parent_death_age", "childhood_parent_death",
  "history_physical_abuse", "history_sexual_abuse", "history_emotional_abuse",
  "history_physical_neglect", "history_emotional_neglect", "history_unstable_housing",
  "history_food_insecurity", "current_household_status", "highest_level_of_education",
  "suspension_from_school", "expulsion_from_school", "behavioral_problems_in_school",
  "academic_problems_in_school", "history_of_bullying", "history_of_being_bullied",
  "current_employment_status", "primary_industry_of_employment", "current_marital_status",
  "current_psychiatric_diagnosis", "current_psychiatric_medications",
  "history_of_suicide_thoughts", "history_of_self_harm_behavior", "history_of_violence",
  "substance_use_disorder_diagnosis", "type_of_substance_used",
  "prior_psychiatric_diagnosis", "prior_diagnosis", "current_medications",
  "history_of_prior_charges", "history_of_prior_convictions", "depressive_symptoms",
  "manic_symptoms", "anxiety_symptoms", "PTSD_symptoms", "psychotic_symptoms",
  "suicidal_ideation_behavior", "agitated_behavior", "violence_agression",
  "factual_understanding", "rational_understanding", "ability_to_assist_in_own_defense",
  "competent_to_stand_trial", "restorable_if_incompetent"
)

all_vars <- c(numeric_vars, categorical_vars)

# Generate results for everything
all_results <- map_dfr(all_vars, ~ compare_agreement(df_combined, .x))

# ---------------------------------------------------------
# FILTERING & REPORTING
# ---------------------------------------------------------

# Define the exceptions to pull out of the main report
legal_competency_vars <- c(
  "factual_understanding", "rational_understanding", 
  "ability_to_assist_in_own_defense", "competent_to_stand_trial", 
  "restorable_if_incompetent"
)

free_text_identifiers <- c(
  "examiner", "evaluation_location", "current_charges")

# Split into distinct tables
main_table <- all_results |> 
  filter(!Variable %in% c(legal_competency_vars, free_text_identifiers))

legal_competency_table <- all_results |> 
  filter(Variable %in% legal_competency_vars)

identifiers_table <- all_results |> 
  filter(Variable %in% free_text_identifiers)

# Print Tables
cat("\n================ MAIN VARIABLES =================\n\n")
print(main_table, n = Inf)

cat("\n============= LEGAL COMPETENCY (Jasper Pending) =============\n\n")
print(legal_competency_table)

cat("\n============= FREE-TEXT IDENTIFIERS =============\n\n")
print(identifiers_table)

# Save the comprehensive cleaned table
write_csv(all_results, "output/combined_tasks/simplified_agreement_results.csv")