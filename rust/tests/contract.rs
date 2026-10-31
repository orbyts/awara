#[test]
fn shared_contract() {
    let cases: serde_json::Value =
        serde_json::from_str(include_str!("../../tests/cases.json")).unwrap();
    for case in cases.as_array().unwrap() {
        assert_eq!(
            awara::validate(&case["recipe"]).is_empty(),
            case["valid"].as_bool().unwrap(),
            "{}",
            case["name"]
        );
    }
}
