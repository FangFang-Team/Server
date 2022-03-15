package main

import (
	"encoding/json"
	"io/ioutil"

	"github.com/ddliu/go-httpclient"
)

func Do_Classification(url string, image_b64 string) (map[string]interface{}, bool) {
	resp, err := httpclient.Post(url, map[string]string{"image": image_b64})
	var res map[string]interface{}
	if err != nil {
		Log.Errorf("Error to `Post` from url: %s, with Error: %s", url, err.Error())
		return res, false
	}
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		Log.Error("Error to Read from response, with Error: %s", err.Error())
		return res, false
	}
	err = json.Unmarshal(body, &res)
	if err != nil {
		Log.Error("Error to unmarshal from body, with Error: %s", err.Error())
		return res, false
	} else {
		return res, true
	}

}
