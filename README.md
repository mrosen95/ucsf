Note that this program is a very simple solution that relies on regexes and
common template elements to remove PII from amazon forms. It will not scale well
to other PDF types well because of this problem.

We had to rely on this common property because there was no training data for our
problem and the common libraries like scrubadub for python showed little effectiveness
at diagnosing the problems.

The scrubadub code is included as a potential future solution, but for now it
was deemed to have done a poor enough job that it had to be migrated away from.

To run the program we first need to build the docker container.
```
sudo docker build -t redact-pii .
```

Once the docker container is up and running we can run the program via the
following command.
```
sudo docker run -it redact-pii python3 src/main.py --filename=<file_name>
```

We provide some examples in the package of pdfs to run a redaction on
 - files/example1.pdf
 - files/example2.pdf

However if you want to upload more files please run the following command.
```
docker cp <local_file_path> redact-pii:files/<file_name>
```

Additionally once you have run the program you will need to retrieve the file
from the docker container.

```
docker cp redact-pii:redacted/<file_name> <local_file_path>
```
