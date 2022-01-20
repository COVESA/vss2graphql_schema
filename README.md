# **VSS to GraphQL Schema**

Parse Vehicle Signal Specification tree structure to generate a special GraphQL
schema.

## **Translation Rules and Basic Functionality**

The vss2graphql_schema.py program loads the `.vspec` file into the `anytree`
python structure using COVESA's `vss-tools` functions. This structure
is then used to generate a GraphQL schema based on a special set of translation
rules.

### **Queries and Subscriptions**

A GraphQL Query and Subscription fields are created for each root element from
`anytree` structure. In case of having only the `Vehicle` root element, it
generates the following structure on the schema:

```graphql
# GraphQL schema generated file

type Query {
    vehicle: Vehicle
}

type Subscription {
    vehicle: Vehicle
}
```

#### **Delivery Interval Subscription Parameter**

If the command for subscription delivery interval is given,
a special GraphQL enumeration called `SubscriptionDeliveryInterval` will be
generated and a parameter `deliveryInterval` will be put on the `Subscription`
root field. So in case of having only the `Vehicle` root signal on VSS, the
following structure will be generated on the schema:

```graphql
# GraphQL schema generated file

enum SubscriptionDeliveryInterval {
  """Rate limited: 5s between updates"""
  DELIVERY_INTERVAL_5_SECONDS

  """Rate limited: 1s between updates."""
  DELIVERY_INTERVAL_1_SECOND

  """Get all the updates, no rate limit."""
  REALTIME
}

type Subscription {
    vehicle(deliveryInterval: SubscriptionDeliveryInterval! = DELIVERY_INTERVAL_5_SECONDS): Vehicle
}
```

### **Mutations and Inputs**

Mutations are created based on actuators in `vspec` files. If a branch has any
child of type actuator, a mutation will be created for that branch and the input
will be created to modify its actuator children.

```yaml
# VSS file

Vehicle.Body.Door.IsOpen:
  datatype: boolean
  type: actuator
  description: Door open or closed. True = Open. False = Close

Vehicle.Body.Door.IsLocked:
  datatype: boolean
  type: actuator
  description: Door locked or unlocked. True = Open. False = Close
```

generates:

```graphql
# GraphQL schema generated file

type Mutation{
    setVehicleBodyDoor(input: Vehicle_Body_Door_Input): Vehicle_Body_Door
}

input Vehicle_Body_Door_Input{
    IsOpen: Boolean
    isLocked: Boolean
}
```

### **Type generation**

VSS branches and leafs are translated to GraphQL types and fields on the
schema. Branches generate custom types and leafs generates fields with a
special type conversion (please see Data Types Translation subsection ).

Example:

```yaml
# VSS file

Vehicle:
  type: branch
  description: Highlevel vehicle data.

Vehicle.Speed:
  datatype: float
  type: sensor
  unit: km/h
  description: Vehicle speed

Vehicle.Body:
  type: branch
  description: All body components.

Vehicle.Body.BodyType:
  datatype: string
  type: attribute
  description: Body type code as defined by ISO 3779

```

Generates:

```graphql
# GraphQL schema generated file

"""
Highlevel vehicle data.
"""
type Vehicle {
    body: Vehicle_Body

    """ Vehicle speed """
    speed: Float
}

"""
All body components.
"""
type Vehicle_Body {

    """ Body type code as defined by ISO 3779 """
    bodyType: String
}

```

### Data Scalar Types Translation

Scalar types are converted automatically to the respective GraphQL types,
as the table below shows. If nothing is specified, the native types will be used
for conversion, but there is an option to automatically generate custom
scalars.

| VSS datatype | GraphQL Native Type | Custom GraphQL Scalars |
|--------------|---------------------|------------------------|
| int8         |         Int         |          Int8          |
| uint8        |         Int         |          UInt8         |
| int16        |         Int         |          Int16         |
| uint16       |         Int         |         UInt16         |
| int32        |         Int         |          Int32         |
| uint32       |         Int         |         UInt32         |
| int64        |        String       |          Int64         |
| uint64       |        String       |         UInt64         |
| float        |        Float        |          Float         |
| double       |        Float        |          Float         |
| boolean      |       Boolean       |         Boolean        |
| string       |        String       |         String         |

Array VSS datatypes are translated to GraphQL lists.

### **Enumerations**

VSS `allowed` are converted to GraphQL Enums the following way:

```yaml
# VSS file

Vehicle.Body.RefuelPosition:
  datatype: string
  type: attribute
  allowed: ["front_left", "front_right", "middle_left", "middle_right", "rear_left", "rear_right"]
  description: Location of the fuel cap or charge port
```

generates:

```graphql
# GraphQL schema generated file

"""
Location of the fuel cap or charge port
"""
type Vehicle_Body {
    """ Location of the fuel cap or charge port """
    refuelPosition: Vehicle_Body_RefuelPosition_Enum
}

enum Vehicle_Body_RefuelPosition_Enum {
    FRONT_LEFT
    FRONT_RIGHT
    MIDDLE_LEFT
    MIDDLE_RIGHT
    REAR_LEFT
    REAR_RIGHT
}
```

> **Note**: Enum values are transformed: all non-alphanumeric characters are
> transformed into `_`, all letters are uppercased and another underscore is put
> on the beginning if it starts with a number.

### **Min and Max values**

Using `range` directives in GraphQL schema it is possible to reflect `min` and
`max` values specified in VSS in the following manner:

```yaml
# VSS file

Vehicle.CurrentLocation.Latitude:
  datatype: double
  type: sensor
  min: -90
  max: 90
  unit: degrees
  description: Current latitude of vehicle.
```

generates:

```graphql
# GraphQL schema generated file

# This line is generated only once
directive @range(min: Float, max: Float) on FIELD_DEFINITION | ARGUMENT_DEFINITION | INPUT_FIELD_DEFINITION

"""
The current latitude and longitude of the vehicle.
"""
type Vehicle_CurrentLocation {

    """ Current latitude of vehicle. """
    latitude: Float @range(min: -90.0, max: 90.0)
}
```

### **hasPermission Directive**

To regulate access to GraphQL schema fields for clients,
`hasPermissions` directive will be created and used. All VSS leafs
will receive `hasPermissions` declaration of type read, leafs of
type actuator will in addition receive `hasPermissions` declaration
of type write:


```graphql
# GraphQL schema generated file

# This directive and enum is generated only once
enum HasPermissionsDirectivePolicy {
  RESOLVER
  THROW
}
directive @hasPermissions(permissions: [String!]!, policy: HasPermissionsDirectivePolicy) on FIELD_DEFINITION | OBJECT | INPUT_FIELD_DEFINITION

# When an input is generated to a mutation, it receives write permission
input Vehicle_MyBranch {
    myField: Float @hasPermissions(permissions: ["Vehicle.MyBranch.MyField_WRITE"])
}

# When a type field is generated, it receives read permission
type Vehicle_MyBranch {
    myField: Float @hasPermissions(permissions: ["Vehicle.MyBranch.MyField_READ"])
}

```

### **Franca to VSS Layer Input**

This tool can use franca-based Layer files to determine behavior. For more
information on franca-based layers please see the
[layer readme](https://asc-repo.bmwgroup.net/gerrit/ascgit514.genivi.test.franca2vss.mapping.layer)
used to test this tool.

#### **Filtering**

When given the root layer file on the execution command the tree will be
filtered according to the same tree structure on the layer file. For instance
if you want to generate the schema for `Vehicle.CurrentLocation.Latitude` you
will have to have a layer file with the following structure:

```yaml
# Layer file

Vehicle:
    CurrentLocation:
        Latitude:
            <your layer info>
```

#### **Mutations**

Mutations also require a special _FrancaIDL structure informing write
permissions in addition to the `actuator` datatype on VSS. For instance if you
want to have `MySignal` (which is already an actuator) to have a mutation, you
will need to add this `_francaIDL` write method:

```yaml
# Layer file

MySignal:
  _francaIDL:
    methods:
      write:  # This indicates write access, allowing
```

#### **Lists**

By specifying the branch as a list in the layer file, that branch will be set
as a list in the schema, and all the children (and grandchildren and so on) will
have an `id: ID!` field, to specify what index from the list you want to access.
For instance:

```yaml
# VSS file
Vehicle.Chassis.Axle:
  type: branch
  description: Axle signals

Vehicle.Chassis.Axle.myAxleSignal:
  datatype: string
  type: sensor
  description: myAxleSignal
```

```yaml
# Layer file
Vehicle:
    Chassis:
        - Axle:
            myAxleSignal:
                <your layer info>
```

```graphql
# GraphQL schema generated file

type Vehicle_Chassis {
    axle: [Vehicle_Chassis_Axle]
}
type Vehicle_Chassis_Axle {
    myAxleSignal: String
    id: ID!
}
```

#### **Parent Attributes on mutations**

On the layer file you can also point to a leaf and say it to resolve in the
immediate parent by using the `_parentAttribute` structure. For instance if you
want to `MyParentAttr1` to be resolved in the mutation of Vehicle:

```yaml
# Layer file

Vehicle:
  MyResolvableBranch:
    _francaIDL:
      methods:
        write:
          <your layer info>
    MyParentAttr1:
      _parentAttribute:
    MyParentAttr2:
      _parentAttribute:
    MyParentAttr3:
      _parentAttribute:
  MyLeaf:
    _francaIDL:
      methods:
        write:
          <your layer info>
```

Generates:

```graphql
# GraphQL schema generated file

type Mutation {
    setVehicle(input: Vehicle_Input!): Vehicle
}

input Vehicle_Input {
    MyLeaf: Boolean
    myResolvableBranch: Vehicle_MyResolvableBranch_Input

input Vehicle_MyResolvableBranch_Input {
    MyParentAttr1: Boolean
    MyParentAttr2: Boolean
    MyParentAttr3: Boolean
}
```

## **Getting Started**

For this project you will need to have:
- Python 3.8.5 or later
- Pip
- Pipenv


### **Python Installation On Linux (or mac)**

If you don't have Python installed already I suggest you to use
[pyenv](https://github.com/pyenv/pyenv#installation) to install Python by using
this following command:

```bash
pyenv install <desired py version>
```

Then in this repo's folder there should be a `.python-version` file that describes
the version of python to be used, in our repo there is this file with the version 3.8.5
written. If you want to create this file by yourself and use a specific version you can run:
```bash
pyenv local <desired py version>
```

### **Pip Installation on Linux**

Make sure you have pip installed too. To check you can run

```bash
python3 -m pip -V
```

and see the version of your pip. Make sure your pip is updated with

```bash
python3 -m pip install --upgrade pip
```

If you don't have you can install with
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --force-reinstall
```

### **Pipenv Installation on Linux**

To install Pipenv just run
```bash
python3 -m pip install --user pipenv
```
And pipenv will be installed as a python package under the `--user` flag and you
will be able to run `python3 -m pipenv --help`.

It is a good practice to set on your `.bashrc` (or other, see note 2), the
variable which configures `PIPENV` to always create the virtual environment
inside a `.env` folder the project.

```bash
echo "export PIPENV_VENV_IN_PROJECT=1" >> ~/.bashrc
source ~/.bashrc
```

> **Note 1:**
> When you install pipenv using pip with `--user` flag, you are installing
> pipenv under a folder `.local` under your home directory, so if your system
> does not recognize pipenv as a command, it's maybe because your `$PATH`
> variable does not see this `.local` folder. One alternative is to add this
> line to your `.bashrc` (or similar please see note 2) file as follows:
> ```bash
> echo "export PATH=$PATH:$HOME/.local/bin" >> ~/.bashrc
> source ~/.bashrc
> ```
> and you will be able to run pipenv directly. If you prefer you can always
> just use:
> ```bash
> python3 -m pipenv
> ```
> when you want to just run pipenv

> **Note 2:**
> Every time `.bashrc` is referred here in this file, we are talking about the
> file that runs when your terminal is open, this file may change depending on
> the system and what shell you are using, this may be `~/.bash_profile` or
> `./zsh`.

## **Installation of VSS2GraphQL_Schema**

To install the project and dependencies you can run the following command:

```bash
pipenv sync
```

This command will install this package and its dependencies under your pipenv
isolated environment (`.env` folder if you followed Note 1). Then you can run
commands of this environment with `pipenv run <command in environment>`.

## **Execution of VSS2GraphQL_Schema**

To run the program please `cd` to root path of this project and run:

```bash
pipenv run vss2graphql_schema --help
```

### **Regex filter and match**

These filters will serve to select or remove vss nodes from the schema. The
filter will be used in every node of vss (branches and leafs). Regex filters
will remove nodes (and its children) with qualified name (full lenght name
separated by `_` Eg: Vehicle_Speed) and match will only include nodes that
matches the regex pattern send.

Examples:

```bash
# Including only Vehicle_ADAS (notice that on match you need to match intermediate branches surrounded with ^$ (regex way of saying to match the exact string))
pipenv run vss2graphql_schema --output=resources/schema.graphql --regex-match="^Vehicle$|Vehicle_ADAS" ../resources/spec/VehicleSignalSpecification.vspec

# Excluding Vehicle_ADAS and Vehicle_Powertrain_Transmission (and everything under those branches)
pipenv run vss2graphql_schema --output=resources/schema.graphql --regex-filter="Vehicle_ADAS|Vehicle_Powertrain_Transmission" ../resources/spec/VehicleSignalSpecification.vspec

```

> **Note:**
> If the file is empty while using regex match, please consider that you may be
> not matching any complete path to a leaf with your regex pattern.


## **Contribution to the Development of VSS2GraphQL_Schema**

To install dev packages one may run:

```bash
pipenv sync -d
```

### **Linting**

One may format with autopep8 with command-line:

```bash
autopep8 --in-place --aggressive --aggressive file.py
```

And to check linting you can run:

```bash
pipenv run flake8 --config setup.cfg file.py
```

### **Check Typing**

To use mypy you can run:

```bash
pipenv run mypy --config-file ./setup.cfg file.py
```

### **Tests**

To run nosetests you can run:

```bash
pipenv run nosetests --with-doctest file.py
```
