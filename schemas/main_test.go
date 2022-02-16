package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestValidSchema(t *testing.T) {
	err := loadSchemaFromFile("testdata/1.9.0", "")
	assert.NoError(t, err)

	err = loadSchemaFromFile("testdata/1.9.0", "1.9.0")
	assert.NoError(t, err)
}

func TestInvalidSchemas(t *testing.T) {
	files := []string{
		"invalid_fileformatnumber.yaml",
		"invalid_url.yaml",
		"invalid_scheme.yaml",
		"invalid_host.yaml",
		"invalid_verinurl.yaml",
		"invalid_missingver.yaml",
		"invalid_ver_too_new.yaml",
	}

	for _, file := range files {
		err := loadSchemaFromFile("testdata/"+file, "1.9.0")
		assert.Error(t, err)
	}
}
