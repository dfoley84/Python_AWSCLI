# Python version to build
PYTHON_VERSION = 3.11.5
PYTHON_MAJOR = 3
PYTHON_MINOR = 11
PYTHON_PATCH = 5

# Directories
BUILD_DIR = build
DOWNLOAD_DIR = $(BUILD_DIR)/download
SOURCE_DIR = $(BUILD_DIR)/Python-$(PYTHON_VERSION)
INSTALL_DIR = $(BUILD_DIR)/python-$(PYTHON_VERSION)-install

# Default target
.PHONY: all
all: install

# Download Python source
$(DOWNLOAD_DIR)/Python-$(PYTHON_VERSION).tar.xz:
    @mkdir -p $(DOWNLOAD_DIR)
    @echo "Downloading Python $(PYTHON_VERSION)..."
    @curl -o $@ https://www.python.org/ftp/python/$(PYTHON_VERSION)/Python-$(PYTHON_VERSION).tar.xz

# Extract source
$(SOURCE_DIR)/configure: $(DOWNLOAD_DIR)/Python-$(PYTHON_VERSION).tar.xz
    @mkdir -p $(SOURCE_DIR)
    @echo "Extracting Python source..."
    @tar -xf $< -C $(BUILD_DIR)
    @touch $@

# Configure build
$(SOURCE_DIR)/Makefile: $(SOURCE_DIR)/configure
    @echo "Configuring Python build..."
    @cd $(SOURCE_DIR) && ./configure \
        --prefix=$(INSTALL_DIR) \
        --enable-optimizations \
        --with-ensurepip=install

# Build Python
$(SOURCE_DIR)/python: $(SOURCE_DIR)/Makefile
    @echo "Building Python..."
    @cd $(SOURCE_DIR) && make -j$(shell nproc)
    @touch $@

# Install Python
$(INSTALL_DIR)/bin/python$(PYTHON_MAJOR): $(SOURCE_DIR)/python
    @echo "Installing Python..."
    @cd $(SOURCE_DIR) && make install
    @echo "Python $(PYTHON_VERSION) installed to $(INSTALL_DIR)"

# Create a virtual environment
venv: $(INSTALL_DIR)/bin/python$(PYTHON_MAJOR)
    @echo "Creating virtual environment..."
    @$(INSTALL_DIR)/bin/python$(PYTHON_MAJOR) -m venv venv
    @echo "Virtual environment created at venv/"

# Shortcut targets
.PHONY: download extract configure build install clean help

download: $(DOWNLOAD_DIR)/Python-$(PYTHON_VERSION).tar.xz
extract: $(SOURCE_DIR)/configure
configure: $(SOURCE_DIR)/Makefile
build: $(SOURCE_DIR)/python
install: $(INSTALL_DIR)/bin/python$(PYTHON_MAJOR)

# Clean build artifacts
clean:
    @echo "Cleaning build directory..."
    @rm -rf $(BUILD_DIR)
    @echo "Cleaned."

# Help message
help:
    @echo "Makefile for building Python $(PYTHON_VERSION) from source"
    @echo ""
    @echo "Targets:"
    @echo "  download  - Download Python source"
    @echo "  extract   - Extract source tarball"
    @echo "  configure - Configure build options"
    @echo "  build     - Compile Python"
    @echo "  install   - Install Python to $(INSTALL_DIR)"
    @echo "  venv      - Create a virtual environment with the built Python"
    @echo "  clean     - Remove build artifacts"
    @echo "  help      - Show this help message"
    @echo ""
    @echo "To build and install Python, simply run 'make'"