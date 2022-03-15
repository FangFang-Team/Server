package main

type Server struct {
	IP   string `toml:"ip"`
	Port int    `toml:"port"`
}

type OuterApi struct {
	Classification string `toml:"classification"`
	Label          string `toml:"label"`
}

type InnerApi struct {
	URL            string `toml:"url"`
	Port           int    `toml:"Port"`
	Classification string `toml:"classification"`
	Label          string `toml:"label"`
}

type Logger struct {
	FilePath string `toml:"file_path"`
	LogLevel string `toml:"log_level"`
}

type Config struct {
	Logger    Logger
	Server    Server
	OuterApis OuterApi `toml:"outer_api"`
	InnerApi  InnerApi `toml:"inner_api"`
}
