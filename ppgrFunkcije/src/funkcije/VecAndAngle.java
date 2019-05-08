package funkcije;

public class VecAndAngle {
    public double[][] axis;
    public double angle;

    public VecAndAngle(){
        axis = new double[3][1];
        axis[0][0] = 0.0;
        axis[1][0] = 0.0;
        axis[2][0] = 0.0;
        angle=0.0;

    }
    public double length(){
        return Math.sqrt(axis[0][0]*axis[0][0]+axis[1][0]*axis[1][0]+axis[2][0]*axis[2][0]);
    }

    public void print(){
        //      System.out.printf("Vector --- Length %.4f\n",this.length());
        System.out.printf("Vector: (%.4f, %.4f, %.4f)", axis[0][0], axis[1][0], axis[2][0]);
        System.out.println();
        System.out.printf("Angle: %.4f" , angle);
        System.out.println();

    }
}