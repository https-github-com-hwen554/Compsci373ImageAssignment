**1.**Write a function colinear(), that takes as parameters three 3D vectors representing points, and returns a boolean: true if all three points lie on the same line, false otherwise. Your function should have the following signature:

bool colinear(Vector3 p, Vector3 q, Vector3 r)

You can assume that Vector3 is a class that represents a 3D vector, and exposes fields named x, y, and z, and that the following functions are available to you:

double dot(Vector3 u, Vector3 v) //dot product

Vector3 cross(Vector3 u, Vector3 v) //cross product

You can assume that the Vector3 class has the following member functions available to you:

Vector3 Vector3.normalized() //returns a vector pointing in the same direction with length 1

double Vector3.magnitude() //returns the length of the vector

You can assume that the Vector3 class supports the following operators:

Vector3 + Vector3

Vector3 - Vector3

answer:
```
bool colinear(Vector3 p, Vector3 q, Vector3 r){
    Vector3 d1=p-q;
    Vector3 d2 = p-r;
    if(cross(d1,d2).magnitude()==0){
        return true;
    }else{
        return false;
    }
}
```

**2.**Write a function surfaceNormal(), which takes as parameters an array of 3D vectors representing the vertices of an arbitrarily shaped polygon, and an integer representing the number of vertices that make up the polygon. Your function should compute and return a unit vector that best represents the surface normal of the polygon.

You should assume that vertices are given in anticlockwise order, and that front faces are determined using anticlockwise winding order.

You should not assume that the polygon is well formed. Vertices may be co-linear, and they are not necessarily co-planar.

Your function should have the following signature:

Vector3 surfaceNormal(Vector3 vertices[], int numVertices)

You can assume that Vector3 is a class that represents a 3D vector, and exposes fields named x, y, and z, and that the following functions are available to you:

double dot(Vector3 u, Vector3 v) //dot product

Vector3 cross(Vector3 u, Vector3 v) //cross product

You can assume that the Vector3 class has the following member functions available to you:

Vector3 Vector3::normalized() //returns a vector pointing in the same direction with length 1

double Vector3::magnitude() //returns the length of the vector

You can assume that the Vector3 class supports the following operators:

Vector3 + Vector3

Vector3 - Vector3

Vector3 * double

answer:
```
Vector3 surfaceNormal(Vector3 vertices[], int numVertices){
   Vector3 vec(0,0,0);
   for(int i=0;i<numVertices;i++){
       int pre=i==0?(numVertices-1):(i-1);
       int next=i==(numVertices-1)?0:i+1;
       Vector3 m1=vertices[pre]-vertices[i];
       Vector3 m2=vertices[i]-vertices[next];
       vec=vec+cross(m1,m2);
   }
   
   return vec.normalized();
}
```

**3.**Write a function drawGrid(), that generates the image below:
![alt text](https://s2.loli.net/2022/07/06/bihF1zlv35N4tPg.png)

Your function should have the following signature:

void drawGrid(double width, double height)

The grid consists of rows/columns of squares that span the x-z plane, with each square being made up of two triangles. The width parameter gives the number of of squares the grid contains on the x-axis, and the height parameter gives the number of squares the grid contains on the z-axis.

Each square is exactly one unit wide on both the x and z axes.

The y axis value of each vertex is derived from its location on the x and z axes. The y-axis value is equal to the cosine (in radians) of the x-axis value + the cosine (in radians) of the z-axis value.

You must use GL_TRIANGLES to draw the mesh. You do not need to specify vertex colours.

The vertices must be given in anticlockwise order for the triangles as seen from above. In each pair of triangles, the triangle closer to the origin must be drawn starting from the closest vertex to the origin (minimum x and z), and the triangle farther away from the origin must be drawn starting from the farthest vertex from the origin (maximum x and z).

The grid should fill in each column (each group of height tiles that share x-axis values) before proceeding to the next column.

The image above shows the grid drawn in wireframe. You do not need to specify that drawing will be done in wireframe.

You can assume that if required, you have access to a Vector3 class that represents a 3D vector, and exposes fields named x, y, and z.

You can assume that you have access to standard trigonometric functions such as cos(), and that they assume input parameters are in radians by default.

Important note:

Coderunner requires certain OpenGL functions to use special versions:

Instead of glVertex3d(), use CRVertex3d()

answer:
```
void drawGrid(double width, double height){
     glBegin(GL_TRIANGLES);
        for(double m1 = 0; m1 < width;m1+=1)
    {
        for(double n1 = 0; n1 < height;n1+=1)
    {
        CRVertex3d(m1,cos(m1)+cos(n1),n1);
        CRVertex3d(m1,cos(m1)+cos(n1+1),n1+1);
        CRVertex3d(m1+1,cos(m1+1)+cos(n1),n1);
        CRVertex3d(m1+1,cos(m1+1)+cos(n1+1),n1+1);
        CRVertex3d(m1+1,cos(m1+1)+cos(n1),n1);
        CRVertex3d(m1,cos(m1)+cos(n1+1),n1+1);
    }
}
        glEnd();
}

```

**4.**Write a function projectVertex(), that computes the projection of a vertex on to a plane for the purpose of creating a shadow.

The plane is given in the form ax + by + cz + d = 0

Your function should have the following signature:

Vector3 projectVertex(Vector3 vertex, double a, double b, double c, double d)

The function should return the location of a vertex given by the vertex parameter when projected from the origin on to a plane given by the a, b, c,  & d parameters.

If working correctly, the program will produce the following output:

![alt text](https://s2.loli.net/2022/07/06/g85oVWt9ZTan6JX.png)

You can assume that Vector3 is a class that represents a 3D vector, and exposes fields named x, y, and z.

Your code can assume that this is a straightforward case for generating shadows: the light source (the origin of the projection) is located at (0, 0, 0), and you do not need to account for any transformations on the object.

You do not need to handle the actual display of the object or the shadow, only the calculation of the shadow vertex location.

answer:
```
Vector3 projectVertex(Vector3 vertex, double a, double b, double c, double d){
    double coz = -(d * vertex.z) / ((a*vertex.x) + (b*vertex.y) + (c*vertex.z));
    double coy = -(d * vertex.y) / ((a*vertex.x) + (b*vertex.y) + (c*vertex.z));
    double cox = -(d * vertex.x) / ((a*vertex.x) + (b*vertex.y) + (c*vertex.z));
    
    return Vector3 (cox,coy,coz);
}

```
**5.**Write a function phongDirectionalSource() which implements the achromatic version of the Phong Illumination equation for a directional light source.
If the function is implemented correctly you should get the following result (Note: this image is rendered using only your implementation and does not use OpenGL lights or materials)

![alt text](https://s2.loli.net/2022/07/06/lH5fc8jqvRsbaEP.png)

Your function should have the following signature:

double phongDirectionalSource(double ambientIntensity, double diffuseIntensity, double specularIntensity, double ambientReflecCoef, double diffuseReflecCoef, double specularReflecCoef, double shininess, Vector3 pointOnSurface, Vector3 surfaceNormal, Vector3 incomingLightDirection, Vector3 viewPoint)



A Vector3 class representing a 3D vector is available to you, with the following member functions:

Vector3 Vector3::normalized() //returns a vector pointing in the same direction with length 1

double Vector3::magnitude() //returns the length of the vector

void Vector3::normalize() //normalises the vector (destructive)

In addition, you can assume the + and - operators are available for the Vector3 class.


You can assume that the following functions are also defined:

double dot(Vector3 a, Vector3 b) //returns the dot product of a and b

Vector3 cross (Vector3 a, Vector3 b) //returns the cross product of a and b

double pow(double a, double b) //returns a to the power of b

Hint: The parameter incomingLightDirection refers to the direction of travel of light rays emitted from the light source.

:::danger not right 
answer:
```
double phongDirectionalSource(double ambientIntensity, double diffuseIntensity, double specularIntensity, double ambientReflecCoef, double diffuseReflecCoef, double specularReflecCoef, double shininess, Vector3 pointOnSurface, Vector3 surfaceNormal, Vector3 incomingLightDirection, Vector3 viewPoint){
    
    
    double ambient = ambientIntensity*ambientReflecCoef;
    
    
    Vector3 s =Vector3( pointOnSurface.x-incomingLightDirection.x, pointOnSurface.y-incomingLightDirection.y,  pointOnSurface.z-incomingLightDirection.z);
    Vector3 v =  Vector3(viewPoint.x-pointOnSurface.x , pointOnSurface.y-viewPoint.y , pointOnSurface.z-viewPoint.z );
    Vector3 h = (s.normalized() + v.normalized()).normalized();
    double diffuse = diffuseIntensity*diffuseReflecCoef*dot(surfaceNormal,s) / (s.magnitude() * surfaceNormal.magnitude());
    double specular = specularIntensity*specularReflecCoef * pow(dot(surfaceNormal,h) / (h.magnitude() * surfaceNormal.magnitude()), shininess);
    
    
    
    return ambient + (diffuse + specular);
}

```

:::