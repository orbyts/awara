//! Structural validation for portable creative workflow recipes.
pub const SCHEMA: &str = include_str!("../recipe.schema.json");
/// Return validation errors, or an empty vector for a structurally valid recipe.
pub fn validate(recipe: &serde_json::Value) -> Vec<String> {
    let schema: serde_json::Value = serde_json::from_str(SCHEMA).expect("bundled schema is JSON");
    let validator = jsonschema::validator_for(&schema).expect("bundled schema is valid");
    validator
        .iter_errors(recipe)
        .map(|e| e.to_string())
        .collect()
}
