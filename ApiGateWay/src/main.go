package main

import (
	"fmt"
	"os"

	"github.com/BurntSushi/toml"
	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

var Log = logrus.New()

func parse_config(cfg string) Config {
	if _, err := os.Stat(cfg); err != nil {
		fmt.Printf("Config FIle Path: %s is not available!\n", cfg)
		os.Exit(-1)
	}
	var conf Config

	if _, err := toml.DecodeFile(cfg, &conf); err != nil {
		fmt.Printf("Error to Parse Config File: %s, error: %s", cfg, err.Error())
		os.Exit(-1)
	}
	return conf
}

func init_logger(conf *Config) {
	Log.SetFormatter(&logrus.TextFormatter{
		FullTimestamp:          true,
		TimestampFormat:        "2006-01-02 15:04:05",
		ForceColors:            true,
		DisableLevelTruncation: true,
	})

	level, _ := logrus.ParseLevel(conf.Logger.LogLevel)
	Log.SetLevel(level)
	if conf.Logger.FilePath == "null" {
		Log.SetOutput(os.Stdout)
	} else {
		file, err := os.OpenFile(conf.Logger.FilePath, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0666)
		if err != nil {
			fmt.Printf("Error to write log to file: %s, with error: %s", conf.Logger.FilePath, err.Error())
			os.Exit(-1)
		}
		Log.SetOutput(file)
	}
	gin.DefaultWriter = Log.Out
}

func main() {
	conf := parse_config("cfg.toml")
	init_logger(&conf)

	router := gin.Default()
	router.GET("/", func(ctx *gin.Context) {
		Log.Debugf("Request with IP: %s\n", ctx.ClientIP())
		ctx.JSON(200, gin.H{
			"message": "hello world",
		})
	})

	router.POST(conf.OuterApis.Classification, func(ctx *gin.Context) {
		// body, err := ioutil.ReadAll(ctx.Request.Body)
		// if err != nil {
		// 	Log.Errorf("Error to read body from Requests: %s, With Error: %s", ctx.Request.URL.String(), err.Error())
		// 	return
		// }
		// var image_b64 map[string]string
		// if err := json.Unmarshal(body, &image_b64); err != nil {
		// 	Log.Errorf("Error to transform body to map, Error: %s", err.Error())
		// 	return
		// }
		// uri := fmt.Sprintf("%s:%d%s", conf.InnerApi.URL, conf.InnerApi.Port, conf.InnerApi.Classification)
		// b64, ok := image_b64["image"]
		image_b64 := ctx.PostForm("image")
		if len(image_b64) == 0 {
			Log.Errorf("the Body of request: %s doesn't contains key 'image'", ctx.Request.URL.String())
			return
		}
		uri := fmt.Sprintf("http://%s:%d%s", conf.InnerApi.URL, conf.InnerApi.Port, conf.InnerApi.Classification)
		res, ok := Do_Classification(uri, image_b64)
		if ok {
			ctx.JSON(200, res)
		} else {
			ctx.JSON(500, gin.H{
				"message": "Server Internal Error",
			})
		}
		ctx.JSON(200, gin.H{
			"message": "ok",
		})
	})

	server_url := fmt.Sprintf("%s:%d", conf.Server.IP, conf.Server.Port)
	router.Run(server_url)
}
