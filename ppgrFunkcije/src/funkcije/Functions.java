package funkcije;

import static java.lang.Math.*;

public class Functions {

    // pomocne f-je:

    public static void printMatrix(double[][] matrix) {
        //    System.out.println("**************************************");
        for (int row = 0; row < matrix.length; row++) {
            for (int col = 0; col < matrix[row].length; col++) {
                System.out.printf("%.4f", matrix[row][col]);
                System.out.print("   ");
            }
            System.out.println();
        }
        //   System.out.println("**************************************");
    }

    public static double[][] alfaMatrix(Double alpha){
        double [][] result = new double[3][3];

        result[0][0] = 1.0;
        result[0][1] = 0.0;
        result[0][2] = 0.0;

        result[1][0] = 0.0;
        result[1][1] = cos(alpha);
        result[1][2] = -sin(alpha);

        result[2][0] = 0.0;
        result[2][1] = sin(alpha);
        result[2][2] = cos(alpha);

        return result;
    }

    public static double[][] betaMatrix(Double beta){
        double [][] result = new double[3][3];

        result[0][0] = cos(beta);
        result[0][1] = 0.0;
        result[0][2] = sin(beta);

        result[1][0] = 0.0;
        result[1][1] = 1.0;
        result[1][2] = 0.0;

        result[2][0] = -sin(beta);
        result[2][1] = 0.0;
        result[2][2] = cos(beta);

        return result;
    }

    public static double[][] gamaMatrix(double gama){
        double [][] result = new double[3][3];

        result[0][0] = cos(gama);
        result[0][1] = -sin(gama);
        result[0][2] = 0.0;

        result[1][0] = sin(gama);
        result[1][1] = cos(gama);
        result[1][2] = 0.0;

        result[2][0] = 0.0;
        result[2][1] = 0.0;
        result[2][2] = 1.0;

        return result;
    }

    public static double[][] multiply3x3(double[][] matrixA,double[][] matrixB){
        double [][]  result = new double[3][3];
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++){
                for(int k=0;k<3;k++){
                    result[i][j] += matrixA[i][k]*matrixB[k][j];
                }
            }
        }
        return result;
    }

    public static double[][] normalizeVec(double[][] vec){
        double [][] newvec = new double[3][1];
        double length = sqrt( vec[0][0]*vec[0][0]+vec[1][0]*vec[1][0]+vec[2][0]*vec[2][0]);
        newvec[0][0] = vec[0][0] / length;
        newvec[1][0] = vec[1][0] / length;
        newvec[2][0] = vec[2][0] / length;

        return newvec;
    }

    // ******************* FUNKCIJE 1-6 *************************

    public static double[][] eulerToA(double angle1, double angle2, double angle3){
        double [][]  a1 = multiply3x3(gamaMatrix(angle3),betaMatrix(angle2));
        double [][]  a2  = multiply3x3(a1,alfaMatrix(angle1));

        return a2;
    }

    public static VecAndAngle AxisAngle(double[][] matrixA){
        VecAndAngle vectorAndAngle= new VecAndAngle();
        vectorAndAngle.axis[0][0] = matrixA[2][1] - matrixA[1][2];
        vectorAndAngle.axis[1][0] = matrixA[0][2] - matrixA[2][0];
        vectorAndAngle.axis[2][0] = matrixA[1][0] - matrixA[0][1];
        vectorAndAngle.axis = normalizeVec(vectorAndAngle.axis);
        double trace = matrixA[0][0]+matrixA[1][1] + matrixA[2][2];
        vectorAndAngle.angle = acos((trace-1.0)/2);

        return vectorAndAngle;
    }

    public static double[][] rodrigez(double[][] vec,double angle ){
        double[][] result = new double[3][3];
        double cos = cos(angle);
        double sin = sin(angle);

        result[0][0] = cos + vec[0][0]*vec[0][0]*(1-cos);
        result[0][1] = vec[0][0]*vec[1][0]*(1-cos)-vec[2][0]*sin;
        result[0][2] = vec[0][0]*vec[2][0]*(1-cos)+vec[1][0]*sin;

        result[1][0] = vec[0][0]*vec[1][0]*(1-cos)+vec[2][0]*sin;
        result[1][1] = cos + vec[1][0]*vec[1][0]*(1-cos);
        result[1][2] = vec[1][0]*vec[2][0]*(1-cos)-vec[0][0]*sin;

        result[2][0] = vec[0][0]*vec[2][0]*(1-cos)-vec[1][0]*sin;
        result[2][1] = vec[1][0]*vec[2][0]*(1-cos)+vec[0][0]*sin;
        result[2][2] = cos + vec[2][0]*vec[2][0]*(1-cos);

        return result;
    }

    public static double[] aToEuler(double[][] matrixA){
        double[] result = new double[3];
        double a31 = matrixA[2][0];
        if (a31< 1 ){
            if ( a31 > -1 ){  // unique
             //   System.out.println("unique");
                result[2] = atan2(matrixA[1][0],matrixA[0][0]);
                result[1] = asin(-a31);
                result[0] = atan2(matrixA[2][1],matrixA[2][2]);
            } else {
            //    System.out.println(" non unique");
                result[2] = atan2(-matrixA[0][1],matrixA[1][1]);
                result[1] = PI/2.0;
                result[0] = 0.0;
            }
        } else{
          //  System.out.println("not unique Ox3 = Oz");
            result[2] = atan2(-matrixA[0][1],matrixA[1][1]);
            result[1] = -PI / 2.0;
            result[0] = 0.0;
        }
        return result;
    }

    public static double[] axisAngle2Q (double [][] vec, double angle) {
        double[] result = new double[4];
        double[][] rotation = rodrigez(vec, angle);
        double[] angles = aToEuler(rotation);

        double calpha = cos(angles[0] * 0.5);
        double salpha = sin(angles[0] * 0.5);

        double cbeta = cos(angles[1] * 0.5);
        double sbeta = sin(angles[1] * 0.5);

        double cgama = cos(angles[2] * 0.5);
        double sgama = sin(angles[2] * 0.5);

        result[0] = salpha * cbeta * cgama - calpha * sbeta * sgama;
        result[1] = calpha * sbeta * cgama + salpha * cbeta * sgama;
        result[2] = calpha * cbeta * sgama - salpha * sbeta * cgama;
        result[3] = calpha * cbeta * cgama + salpha * sbeta * sgama;

        return result;
    }

    public static VecAndAngle q2AxisAngle(double[] q){
        double [] angles = new double[3];
        angles[0] = atan(2*(q[3]*q[0]+q[1]*q[2])/(1-2*(q[0]*q[0]+q[1]*q[1])));
        angles[1] = asin(2*(q[3]*q[1]-q[2]*q[0]));
        angles[2] = atan(2*(q[3]*q[2]+q[0]*q[1])/(1-2*(q[1]*q[1]+q[2]*q[2])));

        return AxisAngle(eulerToA(angles[0], angles[1], angles[2]));
    }

    public static double[] normalizeQ ( double q[]  ){
        double norm = sqrt(q[0]*q[0]+q[1]*q[1]+q[2]*q[2]+q[3]*q[3]);
        double[] nq = new double[4];

        for (int i=0;i<4;i++) {
            nq[i] = q[i] / norm;
        }

        return nq;
    }

    public static double[] negateQ(double[] vec){
        double[] result = new double[4];
        for ( int i=0; i< 4; i++) {
            result[i] = -vec[i];
        }

        return result;
    }

    public static double dotProduct(double[]q1, double[] q2) {
        double sum = 0.0;

        for(int i=0; i<4; i++){
            // System.out.printf(" q1[i] = %.4f q2[2] = %.4f \n",q1[i],q2[i]);
            sum = sum + q1[i]*q2[i];
        }

        return sum;
    }
    // SLerp f-ja
    public static double[] slerp(double[] q1, double[] q2, double tm, double t) {

        double[] qn1= normalizeQ(q1);
        double[] qn2=normalizeQ(q2);
        double cos = dotProduct(qn1,qn2);
        if( cos < 0.0 ){
            q1= negateQ(q1);
            cos = -cos;
        }

        if ( cos > 0.95 ){
            return q1;
        }
        double angle = acos(cos);
        double a = sin(angle*(1-t/tm))/sin(angle);
        double b= sin(angle*t/tm)/sin(angle);
        double[] result = new double[4];
        for (int i=0;i<4;i++){
            result[i] = a*q1[i]+b*q2[i];
        }
        return result;
    }

    // testiranje f-ja
    public static void main(String[] args){

        // test primer uglovi
        double phi = -atan(1.333333333);
        double theta = -asin(0.625);
        double psi = atan(2);
        System.out.printf("Euler angles: phi = %.4f , theta = %.4f , psi = %.4f\n\n", phi, theta, psi);

        double[][] a = eulerToA (phi, theta, psi);
        System.out.println("1) Matrix A = Rx(phi)*Ry(theta)*Rz(psi):\n ");
        printMatrix(a);

        VecAndAngle vanda = AxisAngle(a);
        System.out.println("\n2) Vector p and angle phi: ");
        vanda.print();

        double[][] end = rodrigez(vanda.axis,vanda.angle);
        System.out.println("\n3) Rodrigez:");
        printMatrix(end);

        double[] angles = aToEuler(end);
        System.out.printf("\n4) Angles: \nphi = %.4f , theta = %.4f , psi = %.4f  \n", angles[0], angles[1], angles[2]);
        // provera da li se poklapaju
        //  System.out.printf(" \nphi = %.4f , theta = %.4f , psi = %.4f  \n", phi, theta, psi);

        double[] q = axisAngle2Q(vanda.axis, vanda.angle);
        System.out.printf("\n5) Q:\nq = (%.4f, %.4f, %.4f, %.4f)\n", q[0], q[1], q[2], q[3]);

        VecAndAngle vanda1 = q2AxisAngle(q);
        System.out.println("\n6) Vector p and angle phi: ");
        vanda1.print();


    }
}