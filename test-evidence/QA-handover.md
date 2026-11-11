# Initial QA testing and developer handover

Tester: Denver Hepburn
Date: 11 November 2026
Branch: Quality-Assurance-Denver
Commit containing the tested code and initial evidence: 697b755

## Testing completed

I completed the assertions in the supplied smoke, unit and integration
test files and ran them separately, in that order.

Testing used Windows, Git Bash, Python 3.12.10 and a virtual environment
named .venv312. Scikit-learn 1.6.1 was installed to match the version
recorded in the supplied model.

The missing app.py and requirements.txt files were restored using the
uploaded starter project. The application defects were retained for
the initial tests.

Eight tests ran: four passed and four failed.

| Test | Expected result | Actual result | Status |
|---|---|---|---|
| Home route | HTTP status 200 | HTTP status 200 | Pass |
| Input form | Form and expected input fields are present | Required content found | Pass |
| Model loading | Model loads and has a callable predict method | Checks passed | Pass |
| Missing wind_speed | Error message and no prediction | Error displayed; no prediction | Pass |
| Clear classification | clear | cloudy | Fail |
| Rainy classification | rainy | cloudy | Fail |
| Foggy classification | foggy | cloudy | Fail |
| Valid form submission | Prediction and prediction time displayed without an input error | Input error page returned | Fail |

The smoke tests show that the home route and form work. They do not
confirm that the model produces correct predictions.

## D01 — Classification output is fixed to cloudy

Affected file: app.py
Affected function: classify_weather()
Priority: High
Status: Open

The function obtains prediction_index from the model but does not use
it when selecting the weather label. Instead, it uses:

prediction = weather_classes[1]

This always selects cloudy after a successful model prediction.
The clear, rainy and foggy classification tests therefore fail.

Suggested developer action:
Use the model's predicted class to select the corresponding weather
label, checking that the class-to-label mapping is correct.

Retest:
Run all unit tests again. The clear and rainy examples should return
their expected labels. Investigate D03 separately for the foggy example.

## D02 — Valid form input is passed to the model as strings

Affected file: app.py
Affected function: home()
Priority: High
Status: Open

Temperature, pressure, humidity, wind speed and wind direction are
read from the form without conversion to numbers. When combined with
the other values, the NumPy array contains strings.

The integration test returns an error stating:

dtype='numeric' is not compatible with arrays of bytes/strings.

The response has HTTP status 200, but it contains an error page rather
than a prediction. The test passes its status check, then fails the
check that valid input should not display an error.

The later prediction, valid-class and timing assertions were not
reached during this run.

Suggested developer action:
Convert the form values to numeric values before prediction. Keep
handling for missing and invalid input.

Retest:
Run the integration test again. Valid input should display a recognised
weather class and a non-negative prediction time, without an input
error. Also rerun the missing-field test.

## D03 — Supplied foggy example needs clarification

Affected files: tests/unit_test.py and model/model.pkl
Priority: Medium
Status: Open — clarification needed

The starter instructions expect foggy for this input:

[289.47, 1015, 88, 2, 300, 0, 0, 0, 20]

The local application test returned cloudy. This result alone cannot
establish what the underlying model predicted because D01 forces the
application output to cloudy.

A separate diagnostic check during the project review also returned
model index 1 for this input using scikit-learn 1.6.1. The supplied
weather_classes list maps index 1 to cloudy.

Suggested developer action:
Repeat the direct model check and confirm the intended test input,
model and class mapping with the lecturer. Do not change the expected
result or hard-code a special case simply to make the test pass.

Retest:
After clarification, document any agreed correction and rerun the
classification tests.

## Additional observations

### Model file warning

The test output includes a ResourceWarning for an unclosed model file.

Suggested improvement:
Load the model using a with-open context manager so the file is
explicitly closed afterwards.

### Feature-name warning

The model was trained with feature names but receives a NumPy array
without column names.

Suggested improvement:
Check the expected feature names and order. If named input is used,
ensure that both names and order match the training data.

These warnings are separate from the assertion failures recorded above.

### Temperature units

The form labels temperature as Fahrenheit, while the supplied
integration-test data describes temperature as Kelvin.

Confirm the intended model input units and make the form instructions
consistent with them.

## Evidence

- smoke-before-fixes.txt
- unit-before-fixes.txt
- integration-before-fixes.txt
- Supporting screenshots in this folder

## Developer handover and retesting

The initial tests and evidence are available on Quality-Assurance-Denver.

The assessment specifies QA tests on main and application fixes on a
branch named bugfix. The team should arrange for the reviewed QA work
to reach main before creating or updating the developer's bugfix branch.

After the fixes:
1. Run smoke, unit and integration tests separately.
2. Keep the original logs.
3. Save new results with after-fixes filenames.
4. Record the fix commit and retest outcomes.
5. Update each issue's status based on the evidence.

No application fixes or successful retests are claimed in this document.