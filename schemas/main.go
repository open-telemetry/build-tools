package main

import (
	"flag"
	"fmt"
	"net/url"
	"os"

	"github.com/Masterminds/semver/v3"
	schema "go.opentelemetry.io/otel/schema/v1.0"
	"go.opentelemetry.io/otel/schema/v1.0/types"
)

var schemaFilePath = flag.String("file", "", "Input schema file path")
var schemaVersion = flag.String("version", "", "Expected schema version (optional)")

func loadSchemaFromFile(schemaFilePath string, schemaVersion string) error {
	// Parse the schema file.
	telSchema, err := schema.ParseFile(schemaFilePath)
	if err != nil {
		return err
	}

	// We only support a specific format version.
	if telSchema.FileFormat != "1.0.0" {
		return fmt.Errorf("incorrect schema file format version: %s", telSchema.FileFormat)
	}

	// Check the schema URL.
	u, err := url.Parse(telSchema.SchemaURL)
	if err != nil {
		return err
	}

	const expectedScheme = "https"
	const expectedHost = "opentelemetry.io"

	if u.Scheme != expectedScheme {
		return fmt.Errorf("invalid scheme in: %s, expected %s", telSchema.SchemaURL, expectedScheme)
	}

	if u.Host != expectedHost {
		return fmt.Errorf("invalid host name in: %s, expected %s", telSchema.SchemaURL, expectedHost)
	}

	if schemaVersion != "" {
		// Version check is requested.

		// Check the URL first.
		expectedURL := fmt.Sprintf("https://opentelemetry.io/schemas/%s", schemaVersion)
		if telSchema.SchemaURL != expectedURL {
			return fmt.Errorf("invalid Schema URL: expected %s, got %s", telSchema.SchemaURL, expectedURL)
		}

		// Ensure the version exists in the file.
		_, exists := telSchema.Versions[types.TelemetryVersion(schemaVersion)]
		if !exists {
			return fmt.Errorf("%s does not exist in 'versions' section", schemaVersion)
		}

		thisVer, err := semver.StrictNewVersion(schemaVersion)
		if err != nil {
			return fmt.Errorf(
				"invalid version number %s in the schema file: %w",
				schemaVersion, err,
			)
		}

		// Ensure no other version is newer than the sceham file version.
		for ver := range telSchema.Versions {
			parsedVer, err := semver.StrictNewVersion(string(ver))
			if err != nil {
				return fmt.Errorf(
					"invalid version number %s in the schema file: %w",
					ver, err,
				)
			}

			if parsedVer.GreaterThan(thisVer) {
				return fmt.Errorf(
					"found version number %s in the schema file which is greater than the schema file version %s",
					ver, thisVer.String(),
				)
			}
		}
	}

	return nil
}

func main() {
	flag.Parse()

	if schemaFilePath == nil || *schemaFilePath == "" {
		flag.PrintDefaults()
		os.Exit(1)
	}

	fmt.Printf("Checking schema file %s...", *schemaFilePath)

	err := loadSchemaFromFile(*schemaFilePath, *schemaVersion)
	if err != nil {
		fmt.Printf("\nSchema file is not valid: %v\n", err)
		os.Exit(2)
	}

	fmt.Println(" File is valid.")
}
