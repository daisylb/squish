# Squish

Squish is a web proxy that performs "lossy compression" for HTML. It walks its way through a document tree, aggressively slashing any element or attribute that might trigger extra requests or add unneeded bloat, leaving you with just the page's text and nothing else.

Squish is designed for people faced with a 'net connection that's high-latency, low-bandwidth or likes to drop packets, such as people who are:

- in remote areas or developing countries
- relying on a mobile Internet connection
- being throttled for exceeding their broadband usage, or
- behind a poorly-configured or overloaded school/university/corporate network.

## License

Squish is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Squish is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Squish. If not, see <http://www.gnu.org/licenses/>.
