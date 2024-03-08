#   Copyright The OpenTelemetry Authors
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


class ValidationError(Exception):
    """Exception raised if validation errors occur
    Attributes:
        line -- line in the file where the error occurred
        column -- column in the file where the error occurred
        message -- reason of the error
        fqn -- identifier of the node that contains the error
    """

    def __init__(self, line, column, message, fqn):
        super().__init__(line, column, message, fqn)
        self.message = message
        self.line = line
        self.column = column
        self.fqn = fqn

    def __str__(self):
        return f"{self.message} - @{self.line}:{self.column} ('{self.fqn}')"
