# Build Tarri .pkg on macOS

This environment is Linux, so `.pkg` can't be generated here.
Build it on a macOS machine instead:

```bash
mkdir -p dist/macos/payload
cp -r ../tarri-1.0.0/tarri dist/macos/payload/tarri
cd dist/macos
pkgbuild --root payload \
         --identifier com.tarri.lang \
         --version 1.0.0 \
         --install-location /Applications \
         tarri-1.0.0.pkg
```
