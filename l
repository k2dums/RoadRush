[33mcommit db4d4771d14c1be69ee7962c655bd0116f0141d5[m[33m ([m[1;36mHEAD -> [m[1;32mdocker_deploy[m[33m, [m[1;31morigin/docker_deploy[m[33m)[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:30:00 2023 +0530

    file was thought to be redudant earlier

[33mcommit 7b69432e79945dff49b339c94d0763fb28cc0b5d[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:28:46 2023 +0530

    file is present in the manager folder

[33mcommit 1689543fe6da688e9cde81bbec104a2b5ffd25f2[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:27:26 2023 +0530

    file is present in the manager and controller folders respectively

[33mcommit 0bd7c4e582f435b6366d9005f9b53e9e69eae611[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:27:06 2023 +0530

    file is present in the manager and controller folders respectively

[33mcommit d281cda58bd69d36eff95e48622e978dd42e98ff[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:19:46 2023 +0530

    skeleton for pricing , redudant as going for bidding system

[33mcommit 612c0c84d460f98f2c64355f74b32ce83c31ad41[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:18:27 2023 +0530

    added migrations to ignore

[33mcommit 209246ad3fa3a10832ed6da2e1369c4efa8f6337[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:17:59 2023 +0530

    changed map height to 600px, sendServe() sends test attribute to server rather than search

[33mcommit 5c42c458fbb44edc48dad30bbb1532f74588549a[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:16:21 2023 +0530

     added lign and logout button if user authenticated
    
    added destination lat and long
    
    sendServer() now only sends lat and long

[33mcommit 7610cef23275069623c0e0ff90029033d019b07c[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:13:11 2023 +0530

    class method created for matching cars

[33mcommit fd5e7516dbd8df6f6537ea31480b0cee0810a689[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:11:01 2023 +0530

    added DetailView for returning trip details of the trip

[33mcommit 930a1a3a879b3826c8a77987f412f238b9583a37[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:09:17 2023 +0530

    url paths added

[33mcommit 81481a26f747662594ae769224c38a8e4f18f4a0[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:08:01 2023 +0530

    time_start,time_compeleted has new field parameters such as auto_now_add. duration field has field parameter null and blank.
    
    serialize() has the fields to be returned in dict

[33mcommit 7bc26f9c9d9cc5875905ea569175987e64468eee[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:05:32 2023 +0530

    forms for Trips

[33mcommit dca1a4a7a64e4266df8765c3ac65ff9617efee2a[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:04:31 2023 +0530

    added trips to admin with OSMGeoAdmin

[33mcommit 82ad881b12ff7892ac3104ea2e2457eeac0944ca[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:03:31 2023 +0530

    new views index,rider_test. rider_test_loc() views no longer tkaes username as arg

[33mcommit e84337e5c1bca45146c70ad7c1626ad10f4f63c5[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 13:02:02 2023 +0530

    try and catch for testing if received data in proper format
    
    created conditional block for checking search,bid, endTrip with varied logic

[33mcommit 54c93d3bde0a5292a9b37082be37887b2f00bfb0[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Wed Jul 12 12:59:31 2023 +0530

    added trip to the path

[33mcommit b047fd695ada81cf339bddabca73ed64505f764f[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Tue Jul 11 21:12:57 2023 +0530

    added strategies to the app

[33mcommit 226e09731fe60a881ac0f623f3cc9de6a04ffa79[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Tue Jul 11 21:12:14 2023 +0530

    default path for rider now call views.index()
    
    new test path is rider/test. Removed the username arg from rider/username/test_loc -> rider/test_loc

[33mcommit 2460e6494014a4f7369428e59fc18c6dcfa534e8[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Tue Jul 11 21:07:11 2023 +0530

    a common file import for managers

[33mcommit f396f77e099d3dd6dd7e012a080d81eb1bcee96a[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Tue Jul 11 21:03:50 2023 +0530

    removed proxy model. Added model fields onTrip,currentTrip
    
    serializer() now returns also onTrip and currentTrip fields

[33mcommit 6c1cce88743c6ac48e4217dd2ec8699193464852[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jul 10 18:52:24 2023 +0530

    added the tripsManager files under managers folder

[33mcommit efcd717919548077e661bd84e8f7a97697a51712[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jul 10 18:51:55 2023 +0530

    added the riderManager files under managers folder

[33mcommit 8418a1782790d2b8ecf419b4f4b3e2e068ca68f0[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jul 10 18:51:27 2023 +0530

    added the driverManager files under managers folder

[33mcommit 60af1e694ee6b198c504dc0624801de35e132a5c[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jul 10 18:48:33 2023 +0530

    changed the import direction to DriverController

[33mcommit d6e004e65089de3aa136dbeb2788543a7107588f[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jul 10 18:47:57 2023 +0530

    added the field currentTrip

[33mcommit 0b8e7ff7714c001dd3420f25ac84f2c2708ede5a[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jul 10 18:46:59 2023 +0530

    changed the import direction to DriverController

[33mcommit 17394fd30627584489a49780052566fb6a772e24[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jul 10 18:44:21 2023 +0530

    added carId in the list_display

[33mcommit 884e719ee4bcc312b6597bd7a26f0e3ab21a73dc[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jul 10 18:43:19 2023 +0530

    TripController now under controllers folder

[33mcommit a16da26798f11aa7601e892dc41f0a85e4c746f4[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jul 10 18:42:45 2023 +0530

    RiderController now under controllers folder

[33mcommit fddeb21a0814be28b53482bfd18be00121fbc11f[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jul 10 18:42:18 2023 +0530

    Driver controller now under controller folder

[33mcommit 722fdfd1ca2e3e31dae255e4eb20e05e68ffb0bb[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jul 3 00:33:54 2023 +0530

    common import file for controllers

[33mcommit 31e220caa69a7a678ce0d1a840fca34c9e7d9ab3[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jul 3 00:33:04 2023 +0530

    str representation now returns self.username

[33mcommit b80a0555c0fdb34e08d754f92600584fc4cbba7e[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Tue Jun 27 20:00:23 2023 +0530

    fmore files to ignore

[33mcommit 0ce15def5ce5f8d9f56e059d2475b82b353267fe[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:44:52 2023 +0530

    files for creating db used in the migrations

[33mcommit 51b19e996bbe48e8d7b51e69cce7fd370ade49d4[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:42:27 2023 +0530

    migrations files

[33mcommit 66248282c956a4302b1cec41ea80d434637599d9[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:42:05 2023 +0530

    migrations files

[33mcommit b05235c82eef99dfbd659d32fdcb1bd6b8ac3ee6[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:41:24 2023 +0530

    trips added to the app

[33mcommit 99576a6fbd750eac071d7fcc5964705f972c1f4d[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:40:23 2023 +0530

    changed in loginView return JsonResponse rider to driver, invoked login() in  the registerView()

[33mcommit 89e972c9f2eb46c3b3b27d8a3a5bd6f417492b88[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:38:34 2023 +0530

    get_queryset() minor tweak to the type, added CarTypes Choices

[33mcommit 448f635bd87a456ea508049f20b90266ed1ad7d2[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:36:23 2023 +0530

    added new trip status, and orgin,destination to the model field. Trip Status is now a Choices

[33mcommit ea5d76d1c292105b66bedb3b4652c0c913c95523[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:35:17 2023 +0530

    added the behaviour to createTrip and endTrip

[33mcommit 50593bde5273c1143498cbb07358516af9f68226[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:34:31 2023 +0530

    contains input for long and lat, radio for carType and map for display

[33mcommit 1f4b56fdbf2fc9869c135fde9fb43479a2a76c67[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:33:26 2023 +0530

    changes the type=Password to the password field

[33mcommit 029878ef5085d366122d39330e8d00f2a28263a7[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:32:47 2023 +0530

    added html with basic testing of the backend

[33mcommit d187661e93f80265e5353f1a0711362ea357e158[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:32:00 2023 +0530

    changed the behaviour of test view, added logout amd all_rider View
    
    added decorator @login_required and @csrf_exempt to some functions

[33mcommit 99a34a74a74f8b9152f30d6982a2757113cdc52e[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:30:18 2023 +0530

    changed /test url '', added /all_riders and /logout path

[33mcommit e263c7fe7430c41bc2b4aea8ce0af95b637afd16[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:28:31 2023 +0530

    changed the url parameter from rider_id to rider_name

[33mcommit c3bd909da3ee811306eac33e272ca16d05a65404[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:27:40 2023 +0530

    get_querySet minor tweak to the type, as the User Choices names changed from Types to UserTypes

[33mcommit 6ae091036119a8ca338cac229387b4f97facab82[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:26:24 2023 +0530

    added getRider() returns riderObj

[33mcommit 869bdd6c061604b14113519f0af61a13d3d42c57[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:25:39 2023 +0530

    change self.riderId to rider_name, recieve() now receives newSearch and carType data
    
    added driverSerialization()

[33mcommit 7fab2000f09cbbdf3ce6997d18ef48b272d37f9e[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:21:58 2023 +0530

    use of gis model function Distance to get distance, additional function updateDriverOccupiedStatus_driverObj()
    
    getCars() now takes carType parameter to return cars based on carType

[33mcommit ce52b8768283aa788bbf2f9229af09e501cacbcf[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:18:11 2023 +0530

    now getCard() takes in carTypes as parameter to return the cars based on carType

[33mcommit 8ed48625602398544560c5319f056459b7fb4dad[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:16:52 2023 +0530

    changed the choices name from Types to UserTypes

[33mcommit 3bb49f1a66dd6c4d25152af6a3b26b03525ea813[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Mon Jun 26 22:15:58 2023 +0530

    new path for simple testing

[33mcommit 431f2044c17c429a0b7ba88e6891d84c95f92f3d[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 10 15:14:07 2023 +0530

    removing venv files from remote repo

[33mcommit 61cb82ad46e7297976d520d7ad84673e70c93ef8[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 10 14:31:13 2023 +0530

    adding stratergies files

[33mcommit 8eec02a6916a32249220b9a8b862cd66aa0affb3[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 10 14:20:55 2023 +0530

    module needed for trips

[33mcommit 306446e0b85d15f14cbb1956f1b7ea6e41f88d9c[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Fri Jun 9 21:28:12 2023 +0530

    Added url paths to home path

[33mcommit a8a62d7f11137eb47d20729d2ece927803b14957[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Fri Jun 9 20:07:37 2023 +0530

    venv files

[33mcommit d4bb965e0b832d7e12b1402e0dfbf2c5d8bde4b5[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 3 21:04:01 2023 +0530

    requirements

[33mcommit 4e7714fd437d6c9c63e8f6b7c44b3f5408b55dcc[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 3 21:03:35 2023 +0530

    dataset

[33mcommit c3555fc3065662fd28a3377fe012ec82e7b62ef9[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 3 21:02:37 2023 +0530

    intial migrations

[33mcommit 28538fd13db816835bb9bac0c11064d9480fcaa3[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 3 21:00:24 2023 +0530

    new migrations for testing

[33mcommit 6bffdb9a202569294f3d6e7651b7f742997d6ca3[m[33m ([m[1;31morigin/main[m[33m, [m[1;32mmain[m[33m)[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 3 15:56:03 2023 +0530

    skeleton for location services

[33mcommit d2a2ec4d4ee49a2457ec99f358453c53f7212971[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 3 15:55:11 2023 +0530

    added routing and posgis dependency

[33mcommit 98af4f0728602925e589a2ddab85bca60fd3d873[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 3 15:53:53 2023 +0530

     contains the controller,models,routing for the rider  interface

[33mcommit 28f90de3de327ed63c1a14c9cedd99d1e1007a37[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 3 15:53:32 2023 +0530

     contains the controller,models,routing for the driver interface

[33mcommit b9096d77117af5473542cf60fadc4bed80f685d8[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 3 15:43:33 2023 +0530

    dataset for location points

[33mcommit 54c4f7c0d0a1cb6f7710eb6fb9d7b873cd1c26ae[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 3 15:42:54 2023 +0530

    migrations for loading data

[33mcommit 5a8ea7b0ac2d05ddec40c89e3aabe77ed24b9c19[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 3 15:42:00 2023 +0530

    swagger not used currently

[33mcommit 3072266afd32cac8d0f8c60eb0a5f2a0a90f3d54[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 3 15:41:04 2023 +0530

    registered User

[33mcommit a8b81cf367b49b4e5f0c9e28ad8731100d2c117e[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sat Jun 3 15:36:09 2023 +0530

    UserManager creat_user() password can't be none
    Setting of defauly user.type=None in superUser
    Added User.Types
    Required field included password for creating user

[33mcommit 8eca5ba7c96307e3d54a531ab4f63a8b61ee5097[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sun Feb 26 21:24:50 2023 +0530

    changed the swagger title to RoadRush

[33mcommit 862918a4419d95060be46cd683b18630444ee2f4[m
Author: k2dums <norbu.paddu@gmail.com>
Date:   Sun Feb 26 20:44:05 2023 +0530

    first commit
