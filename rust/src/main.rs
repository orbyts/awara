fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    match args.first().map(String::as_str) {
        Some("--version") => println!("awara 0.0.0"),
        Some("schema") => println!("{}", awara::SCHEMA),
        Some("validate") if args.len() == 2 => {
            let result = std::fs::read_to_string(&args[1])
                .map_err(|e| e.to_string())
                .and_then(|s| serde_json::from_str(&s).map_err(|e| e.to_string()));
            match result {
                Ok(value) => {
                    let errors = awara::validate(&value);
                    if errors.is_empty() {
                        println!("Valid Awara recipe");
                    } else {
                        eprintln!("{}", errors.join("\n"));
                        std::process::exit(1);
                    }
                }
                Err(e) => {
                    eprintln!("{e}");
                    std::process::exit(2);
                }
            }
        }
        _ => {
            eprintln!("Usage: awara validate FILE | schema | --version");
            std::process::exit(2);
        }
    }
}
